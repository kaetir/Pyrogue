"""
- There is two different kind of objects
·         Equipment:
            o   Weapon, that can increases damage and raises characteristics
            o   Armor, raises armor points and characteristics
            o   Jewels. Those can be equipped in different equipment slots (
                 2 slots for weapon: hand left and hand right,
                 2 for jewels,
                 5 for armor: head, chest, pants, arms, legs),
                raising stats or granting power.
·         consumables: that can be used and disappears upon use, and help the player or inflict damage
- Objects have a value of gold, and equipments have a minimum level to equip them.

"""

from random import randint, random


class Item:
    name: str = "caca"

    def __init__(self):
        print("item crée")

    def random(self):
        typ = randint(1, 3)
        if typ == 1:
            # equipement
            return Equipment()
        elif typ == 2:
            # consumable
            return consumables()


class Equipment(Item):
    name = "équipement"


class Weapon(Equipment):
    damage: int = 1
    precission: float = 0.99

    def hit(self) -> int:
        if random() > self.precission:
            return self.damage
        return 0


class Armor(Equipment):
    value: int = 1

    def equiper(self) -> int:
        return self.value


class Jewel(Equipment):
    color: str = "blueje"


class consumables(Item):

    def use(self) -> None:
        print("pouf")
