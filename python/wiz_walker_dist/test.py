#!/usr/bin/env python3

# Copyright 2021 PeechezNCreem
# Licensed under the GPL 3.0.

import asyncio
import ctypes
import math
import os
import signal
import threading
import time

from wizwalker import Keycode, WizWalker
from wizwalker.hotkey import Hotkey, Listener, ModifierKeys

user32 = ctypes.windll.user32


class Quitter(threading.Thread):
    def __init__(self, *, delay=3):
        super().__init__(name="Quitter")
        self.delay = delay

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args, **kwargs):
        time.sleep(self.delay)
        os._exit(0)


class PeechPy:
    DEFAULT_OFFSET = 150
    OFFSET_STEP = 50

    def __init__(self):
        self.walker = WizWalker()

        self.managed_clients = []
        self.offset = PeechPy.DEFAULT_OFFSET

    ### Interface

    async def start(self):
        try:
            await asyncio.wait(
                (
                    client_task := asyncio.create_task(self.client_listener()),
                    hotkey_task := asyncio.create_task(self.hotkey_listener()),
                )
            )
        except (KeyboardInterrupt, asyncio.exceptions.CancelledError):
            pass
        finally:
            await self.stop()

    async def stop(self):
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        with Quitter():
            if self.walker:
                await self.walker.close()

    ### Services

    async def client_listener(self):
        while True:
            for client in self.walker.get_new_clients():
                await client.hook_handler.activate_quest_hook(wait_for_ready=False)
                await client.hook_handler.activate_player_hook(wait_for_ready=False)
                self.managed_clients.append(client)
            await asyncio.sleep(8)

    async def hotkey_listener(self):
        modifiers = ModifierKeys.ALT | ModifierKeys.NOREPEAT
        listener = Listener(
            Hotkey(Keycode.Q, self.teleport, modifiers=modifiers),
            Hotkey(Keycode.E, self.teleport_offset, modifiers=modifiers),
            Hotkey(Keycode.R, self.reset_offset, modifiers=modifiers),
            Hotkey(Keycode.F, self.increase_offset, modifiers=modifiers),
            Hotkey(Keycode.C, self.decrease_offset, modifiers=modifiers),
        )

        while True:
            await listener.listen()
            await asyncio.sleep(0.1)

    ### Hacks

    async def teleport(self):
        if player := self.get_active_client():
            await player.teleport(await player.quest_position.position())

    async def teleport_offset(self):
        if player := self.get_active_client():
            quest_pos = await player.quest_position.position()

            theta = 3 * math.pi / 2 - await player.body.yaw()
            quest_pos.x += self.offset * math.cos(theta)
            quest_pos.y += self.offset * math.sin(theta)

            await player.teleport(quest_pos)

    async def reset_offset(self):
        if self.get_active_client():
            self.offset = PeechPy.DEFAULT_OFFSET

    async def increase_offset(self):
        if self.get_active_client():
            self.offset += PeechPy.OFFSET_STEP

    async def decrease_offset(self):
        if self.get_active_client() and self.offset >= PeechPy.OFFSET_STEP:
            self.offset -= PeechPy.OFFSET_STEP

    ### Utils

    def get_active_client(self):
        target = user32.GetForegroundWindow()
        return next(
            (c for c in self.managed_clients if c.window_handle == target), None
        )


if __name__ == "__main__":
    asyncio.run(PeechPy().start())
