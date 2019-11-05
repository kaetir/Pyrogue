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

    def is_ended(self):
        """
        @summary dit si le mob est mort
        @return: true si le mob est dead
        """
        return not self.m.is_alive()

    def start(self) -> int:
        """
        @summary levelup du mob
        """
        for i in range(self.c.level):
            self.m.level_up()

    def tour(self, action: int):
        """
        @summary fait effectué les actions choisies par les perso
        @param action: int action effectué par le joueur
        """
        # ataque de base
        if action == 0:
            # TODO precision de l'arme
            self.c.inflict_damage(self.m,
                                  self.c.inventory.weapon.damage if self.c.inventory.weapon.damage is not None else 1)
        # spell
        elif action < 4:
            # TODO verif spell
            self.c.inventory.active_spells[action].use(self.c, self.m)

        # consumable
        elif action < 8:
            # TODO verif consumable
            self.c.inventory.active_comsumable[action].use(self.c, self.m)
            self.c.inventory.active_comsumable[action] = None

        if self.m.is_alive():
            self.m.inflict_damage(self.c, random.randrange(self.m))