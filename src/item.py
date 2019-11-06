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
    def __init__(self):
        self.name = ""
        self.item_type = ""
        self.icon_id = 0

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


class Jewel(Equipment):
    item_type = "jewel"
    """ emplacement : 
    jewel1, jewel2
    """
    color: str = "blueje"


class Consumables(Item):
    item_type = "consumable"
    def use(self) -> None:
        print("pouf")


class SpellBook(Item):
    item_type = "spellbook"

    def use(self, source, destination) -> None:
        print("mathémagie")
