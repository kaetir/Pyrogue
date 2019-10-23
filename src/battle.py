""""
- There is 2 type of action during a battle:
·         Attack skills to use
·         Spells to throw, which consume MP
· Actions during battle are in a 4 slots action bar for attacks and spells each,
    so you have to equip those to use them.
    All of those actions are stored in a Book,
    and you can add or remove them from your actions bar when you are not battling.

- Your character can do only do one attack skill per turn, but you can use unlimited amount of spells during your turn
- Monsters have those two type of actions and conditions

"""

import src.character as Character
import src.monster as Monster

class battle:
    c: Character = None
    m: Monster = None
    finished: bool = False

    def __init__(self, c:Character, m:Monster = None) -> None:
        if m is None:
            self.m = Monster()
        else:
            self.m = m
        self.c = c

    def battle(self) -> int:
        return 0

