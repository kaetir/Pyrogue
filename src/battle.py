""""
- There is 2 item_type of action during a Battle:
·         Attack skills to use
·         Spells to throw, which consume MP
· Actions during Battle are in a 4 slots action bar for attacks and spells each,
    so you have to equip those to use them.
    All of those actions are stored in a Book,
    and you can add or remove them from your actions bar when you are not battling.

- Your character can do only do one attack skill per turn, but you can use unlimited amount of spells during your turn
- Monsters have those two item_type of actions and conditions

"""

from src.perso.character import Character
from src.perso.monster import Monster


class Battle:
    c: Character = None
    m: Monster = None
    finished: bool = False

    def __init__(self, c: Character, m: Monster = None) -> None:
        if m is None:
            self.m = Monster()
        else:
            self.m = m
        self.c = c

    def battle(self) -> int:
        return 0
