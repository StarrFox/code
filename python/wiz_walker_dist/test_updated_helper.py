#############################
### Written by Benjamin#8693
###
### Code is not meant to be
### perfect, I know some of
### it is pretty lazy, but
### hey it gets the job done.
#############################

import random
import asyncio
import ctypes

from wizwalker import ClientHandler, Keycode, Hotkey, Listener, ModifierKeys
from wizwalker.errors import AddressOutOfRange, MemoryReadError


class Helper(ClientHandler):
    def __init__(self):
        super().__init__()

        self.hotkey_listener = None
        self._running = False

    def get_focused_client(self):
        forground = ctypes.windll.user32.GetForegroundWindow()

        for client in self.clients:
            if client.window_handle == forground:
                return client

        return None

    async def handle_alt_x_pressed(self):
        print(f"Sending x to all clients")
        for client in self.clients:
            await client.send_key(Keycode.X)

    async def handle_alt_e_pressed(self):
        player = self.get_focused_client()

        if player is None:
            return

        x_offset = random.randrange(-450, 450)
        y_offset = random.randrange(-450, 450)

        quest_xyz = await player.quest_position.position()
        quest_xyz.x += x_offset
        quest_xyz.y += y_offset

        print(f"Teleporting to {quest_xyz}")
        await player.teleport(quest_xyz)

    async def dialog_task(self, client):
        while self._running:
            try:
                while await client.is_in_dialog():
                    print("pressing space")
                    await client.send_key(Keycode.SPACEBAR)

            except (MemoryReadError, AddressOutOfRange):
                pass

            await asyncio.sleep(0.5)

    async def teleport_task(self, client):
        while self._running:
            focused_client = self.get_focused_client()

            if focused_client is not None:
                try:
                    focused_pos = await focused_client.body.position()
                    current_client_pos = await client.body.position()
                
                except MemoryReadError:
                    pass

                else:
                    # I forgot to add compare methods to XYZ
                    if focused_pos.distance(current_client_pos) != 0:
                        await client.teleport(focused_pos)

            await asyncio.sleep(0.5)


    async def run(self):
        print("Preparing")
        self._running = True
        self.get_new_clients()
        await self.activate_all_client_hooks()

        # you can't hold down any modifiers and send X
        alt_x = Hotkey(Keycode.X, self.handle_alt_x_pressed, modifiers=ModifierKeys.NOREPEAT)
        alt_e = Hotkey(Keycode.E, self.handle_alt_e_pressed, modifiers=ModifierKeys.ALT | ModifierKeys.NOREPEAT)

        self.hotkey_listener = Listener(alt_x, alt_e)

        tasks = []

        for client in self.clients:
            tasks.append(asyncio.create_task(self.dialog_task(client)))
            tasks.append(asyncio.create_task(self.teleport_task(client)))

        print("Ready")
        while self._running:
            await self.hotkey_listener.listen()

    async def close(self):
        self._running = False
        await super().close()

        if self.hotkey_listener:
            await self.hotkey_listener.close()


async def main():
    helper = Helper()

    try:
        await helper.run()

    finally:
        print("Closing")
        await helper.close()


# this is not a thread
if __name__ == "__main__":
    asyncio.run(main())
