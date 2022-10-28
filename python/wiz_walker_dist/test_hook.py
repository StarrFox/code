from wizwalker import WizWalker
from wizwalker.windows.memory.hooks import PlayerHook

import logging
logging.getLogger("pymem").setLevel(0)


x = WizWalker()
x.get_clients()

client = x.clients[0]
print(f"{client=}")

memory = client._memory


hook = PlayerHook(memory)

pmm = hook.get_pattern_and_mask()

jump = hook.get_jump_address(pmm[0], "x" * len(pmm[0]), module=pmm[2])
print(f"{jump=} {type(jump)=}")

hook_addr = hook.get_hook_address(200)
print(f"{hook_addr=} {type(hook_addr)=}")
