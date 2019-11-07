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
from src.perso.character import Character


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


class Weapon(Equipment):
    """ emplacement : 
    weapon, shield
    """

    static_equipment_type = ["weapon", "shield"]

    def __init__(self) -> None:
        super().__init__()
        self.equipment_type = choice(self.static_equipment_type)
        self.random_icon()

        self.damage = 1
        self.precision = 0.95
        self.block_chance = 0.10

    def random_icon(self):
        if self.equipment_type == "weapon":
            self.icon_id = choice(items_id["swords"])
        elif self.equipment_type == "shield":
            self.icon_id = choice(items_id["shields"])

    def hit(self) -> int:
        if random() > self.precision:
            return self.damage
        return 0


class Armor(Equipment):
    item_type = "armor"
    """ emplacement : 
    helmet, chest, legs, boots, gloves
    """

    static_equipment_type = ["helmet", "chest", "legs", "boots", "gloves", "amulet", "ring"]

    def __init__(self) -> None:
        super().__init__()
        self.equipment_type = choice(self.static_equipment_type)
        self.random_icon()

        self.armor = 1

    def random_icon(self):
        if self.equipment_type == "helmet":
            self.icon_id = choice(items_id["helmets"])
        elif self.equipment_type == "chest":
            self.icon_id = choice(items_id["chests"])
        elif self.equipment_type == "legs":
            self.icon_id = choice(items_id["legs"])
        elif self.equipment_type == "boots":
            self.icon_id = choice(items_id["boots"])
        elif self.equipment_type == "gloves":
            self.icon_id = choice(items_id["gloves"])
        elif self.equipment_type == "amulet":
            self.icon_id = choice(items_id["amulets"])
        elif self.equipment_type == "ring":
            self.icon_id = choice(items_id["rings"])

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
