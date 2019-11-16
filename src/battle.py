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

import random


class coup:
    def __init__(self, id: int, coupJoueur: int, coupMob: int) -> None:
        self.coupId: int = id
        self.coupMob: int = coupMob
        self.coupJoueur: int = coupJoueur


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
        self.start()

        print("======= AU COMBAT =======")
        self.c.print()
        self.m.print()
        print("=========================")

    def is_ended(self) -> bool:
        """
        @summary dit si le mob est mort
        @return: bool true si le mob est dead
        """
        if not self.m.is_alive():
            self.c.gain_xp(30)
            self.c.armor = self.c.max_armor
            self.c.inventory.money += random.randint(20, 100)
            return True

    def start(self) -> None:
        """
        @summary levelup du mob
        """
        for i in range(self.c.level - 1):
            self.m.level_up()

    def tour(self, action: int) -> [int, int]:
        """
        @summary fait effectué les actions choisies par les perso
        @param action: int action effectué par le joueur
        @return rc, rm : reaction du joueur et reaction monstre
                0 - RIEN
                1 - dodged
                2 - parry
                3 - DANS LE CUL
        """
        # ataque de base
        rc = 0
        rm = 0
        if action == 0:
            dc = self.c.inventory.weapon.damage if self.c.inventory.weapon is not None else 1
            rm = self.c.inflict_damage(self.m, dc)

        # spell
        elif action < 4:
            action -= 1
            # verif spell
            if self.c.inventory.active_spells[action] is None:
                return 0, 0

            if not self.c.inventory.active_spells[action].use(self.c, self.m):
                return 0, 0



        # consumable
        elif action < 8:
            action %= 4

            # verif consumable
            if self.c.inventory.active_comsumable[action] is None:
                return 0, 0

            if self.c.inventory.active_comsumable[action].bonus:
                self.c.inventory.active_comsumable[action].use(self.c)
            else:
                self.c.inventory.active_comsumable[action].use(self.m)

            self.c.inventory.active_comsumable[action] = None

        if self.m.is_alive():
            dm = random.randint(self.m.damage_min, self.m.damage_max)
            rc = self.m.inflict_damage(self.c, dm)

        print("-------------------")
        self.c.print()
        self.m.print()

        return rc, rm
