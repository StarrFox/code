from lark import Lark, Transformer


class LoopCommand:
    def __init__(self, param) -> None:
        self.param = param

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.param=}>"

class MoveCommand(LoopCommand):
    pass


class NpcCommand(LoopCommand):
    pass


class StopCommand(LoopCommand):
    pass


class BattleLoop:
    def __init__(self, commands: list, iterations: int = None) -> None:
        self.commands = commands
        self.iterations = iterations

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.iterations=} {self.commands=}>"


class CombatAction:
    def __init__(self, param, *, source: str = None,  enchant: str = None, maybe_enchant: bool = False) -> None:
        self.param = param
        self.source = source
        self.enchant = enchant
        self.maybe_enchant = maybe_enchant

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.param=} {self.enchant=} {self.maybe_enchant=}>"

    def set_source(self, value):
        self.source = value

    def set_enchant(self, enchant: str, maybe_enchant: bool = False):
        self.enchant = enchant
        self.maybe_enchant = maybe_enchant


class AllyAction(CombatAction):
    pass

class EnemyAction(CombatAction):
    pass

class CardAction(CombatAction):
    pass

class NotargetAction(CombatAction):
    pass


class Battle:
    def __init__(self, actions) -> None:
        self.actions = actions

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.actions=}>"

class WizWalkerScriptTransformaer(Transformer):
    def wizwalker_script(self, sections):
        loop, battle, *move_steps = sections
        print(f"{loop=}", f"{battle=}", f"{move_steps=}", sep="\n\n")
        return loop, battle, move_steps

    def loop(self, loop):
        iterations = None
        commands = []
        for child in loop:
            child = child[0]
            if isinstance(child, int):
                iterations = child

            else:
                commands.append(child)

        return BattleLoop(commands, iterations)

    def loop_iterations(self, iterations):
        return iterations

    def loop_command(self, command):
        return command

    def move_command(self, target):
        return MoveCommand(target[0])

    def stop_command(self, target):
        return StopCommand(None)

    def npc_command(self, target):
        return NpcCommand(None)

    def string_with_numbers(self, data):
        return data[0].value

    def number(self, value):
        return int(value[0].value)

    def name(self, value):
        return value[0].children[0].value

    def cardname(self, value):
        return value[0]

    def xy(self, value):
        x, y = value
        return x, y

    def combat_action(self, value):
        enchant = None
        maybe_enchant = False

        for item in value[2:]:
            if item.data == "maybe_enchant":
                maybe_enchant = True
                enchant = item.children[0]

            elif item.data == "enchant":
                enchant = item.children[0]

        source, action = value[:2]
        action.set_source(source)
        action.set_enchant(enchant, maybe_enchant)
        return action

    def combat_target(self, value):
        return value[0]

    def enemy_target(self, value):
        return EnemyAction(value[0])

    def ally_target(self, value):
        return AllyAction(value[0])

    def card_target(self, value):
        return CardAction(value[0])

    def notarget(self, value):
        return NotargetAction(None)

    def target_param(self, value):
        return value[0]

    def battle(self, value):
        return Battle(value)


grammar = open("wizwalker_script.lark").read()
parser = Lark(grammar)


test = """
[loop 20]
do move 1
do move battle1
do npc
do stop

[battle]
fireblade, ally(self)
meteor, notarget, epic?
firecat, enemy(first), giant
epic, card(meteor)

<move 1>
10, 10
100, 50

<move battle1>
20, 20
"""


parsed = parser.parse(test)

print(
    parsed.pretty()
)

transformed = WizWalkerScriptTransformaer().transform(parsed)

print("\n\ntransformed:\n", transformed)
