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

from __future__ import annotations
from random import randint, random, choice
from res.ressources_id import items_id


class Item:
    def __init__(self):
        self.name = ""
        self.item_type = ""
        self.icon_id = 0
        self.prix = randint(1, 42)

    def get_icon_id(self):
        return self.icon_id

    def set_icon_id(self, icon_id):
        self.icon_id = icon_id

    @staticmethod
    def random():
        # incrémenter le deuxieme paramettre pour ajouter des catégories
        typ = randint(1, 4)
        if typ == 1:
            # equipement
            return Equipment()
        elif typ == 2:
            # consumable
            return Consumables()
        elif typ == 3:
            # speelbook
            return SpellBook()


class Equipment(Item):

    def __init__(self) -> None:
        super().__init__()
        item_type: str = "equipment"
        print(item_type)


class Weapon(Equipment):
    item_type = "weapon"
    """ emplacement : 
    weapon, shield
    """
    damage: int = 1
    precission: float = 0.99

    def hit(self) -> int:
        if random() > self.precission:
            return self.damage
        return 0


class Armor(Equipment):
    item_type = "armor"
    """ emplacement : 
    helmet, chest, legs, boots, gloves
    """

    value: int = 1

    def __init__(self) -> None:
        super().__init__()
        self.armor_type = ""


class Consumables(Item):
    item_type = "consumable"
    bonus: bool = True

    def __init__(self):
        super().__init__()
        self.icon_id = choice(items_id["sandwichs"])

    def use(self, c: Character) -> None:
        if self.bonus:
            c.heal(c.max_health//2)
        print("pouf")


class SpellBook(Item):
    item_type = "spellbook"
    bonus: bool = True

    def use(self, source, destination) -> None:
        print("mathémagie", self.icon_id)
        print("{} use a spell on {}".format(source, destination))
