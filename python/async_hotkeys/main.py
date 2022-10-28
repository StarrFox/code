import os
import asyncio
import ctypes
import ctypes.wintypes
from typing import Coroutine, Callable, List
from enum import IntFlag
from collections import defaultdict
from threading import Thread

import janus

from keycodes import Keycode


user32 = ctypes.windll.user32


class KeyNotFoundError(ValueError):
    def __init__(self, key: str):
        super().__init__(f"Key {key} not found.")


class ModifierKeys(IntFlag):
    ALT = 0x1
    CTRL = 0x2
    NOREPEAT = 0x4000
    SHIFT = 0x4


class Hotkey:
    # TODO: add properties to set attrs after init
    def __init__(self, keycode: Keycode, callback: Coroutine, *, modifiers: ModifierKeys = 0):
        self.keycode = keycode
        self.modifiers = modifiers
        self.callback = callback


class Listener:
    def __init__(self, hotkeys: List[Hotkey], *, loop: asyncio.AbstractEventLoop = None):
        if loop is None:
            loop = asyncio.get_event_loop()

        self.loop = loop

        self.ready = False
        self._hotkeys = hotkeys
        self._callbacks = {}
        self.queue = None
        self.message_task = None

    def listen_forever(self) -> asyncio.Task:
        return asyncio.create_task(self._listen_forever_loop())

    async def _listen_forever_loop(self):
        while True:
            await self.listen()

    async def listen(self):
        """
        Listen for one event
        """
        self.queue = janus.Queue()
        if self.message_task is None:
            self.message_task = self.loop.run_in_executor(None, self._add_and_listen)

        message = await self.queue.async_q.get()
        keycode, modifiers = message.split("|")
        keycode = int(keycode)
        if modifiers == "0":
            modifiers = 0
        else:
            modifiers = ModifierKeys(modifiers)

        # TODO: add to self._tasks and cancel in self.close
        self.loop.create_task(self._callbacks[keycode + modifiers]())

    def _add_and_listen(self):
        if not self.ready:
            self._add_hotkeys()
        self.ready = True

        while True:
            message = ctypes.wintypes.MSG()
            res = user32.GetMessageW(
                ctypes.byref(message),
                None,
                # 0x0312,
                # 0x0313
                0x311,
                0x314
            )

            modifiers = message.lParam & 0b1111111111111111
            keycode = message.lParam >> 16

            self.queue.sync_q.put(f"{keycode}|{modifiers}")

            user32.DispatchMessageW(ctypes.byref(message))

    def _add_hotkeys(self):
        for hotkey in self._hotkeys:
            if self._register_hotkey(hotkey.keycode.value, hotkey.modifiers):
                self._callbacks[hotkey.keycode.value + hotkey.modifiers] = hotkey.callback
            else:
                # TODO: switch error
                raise RuntimeError("oopsie whoopsie")


    def _register_hotkey(self, keycode: int, modifiers: ModifierKeys = 0) -> bool:
        res = user32.RegisterHotKey(
            None,
            1,
            modifiers,
            keycode
        )

        return res != 0


async def main():
    async def callback():
        print("a was pressed")

    hotkey = Hotkey(Keycode.A, callback)
    listener = Listener([hotkey])

    listen_task = listener.listen_forever()

    while True:
        await asyncio.sleep(300)


if __name__ == "__main__":
    asyncio.run(main())
