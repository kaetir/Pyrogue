"""
- Your character have an Inventory which has
·         Objects
·         Your amount of gold
·         Slots
            o   2 slots for weapon: hand left and hand right, increasing damage minimum and maximum and raising stats
            o   2 for jewels raising stats
            o   5 for armor: head, chest, pants, arms, legs), raising stats.
- Your character can equip in equipment slots and increase his stats
- Your character can earn success, he can see which ones he has unlocked, and those which are still locked.
    Success are descriptions for something he has accomplished through all games.
"""

from src.item import *


class Inventory:

    def __init__(self) -> None:
        super().__init__()

        # Rempli d'items
        self.max_size: int = 6 * 8
        self.items: list[Item] = [None] * self.max_size

        # les consumables sont stoké
        # max size 4
        self.active_comsumable: list[Consumables] = [None, None, None, None]

        # Les speels sont tous dans des speels book et on en actives certain
        # max size 3
        self.active_spells: list[SpellBook] = [None, None, None]

        self.helmet = None
        self.chest = None
        self.legs = None
        self.boots = None
        self.gloves = None
        self.weapon = None
        self.shield = None
        self.amulet = None
        self.ring = None

        # LA THUNE
        self.money: int = 0

    def equip(self, item):
        """
        @summary equipe un objet et l'enleve de l'inventaire si il est dedans
        @param item: item a equiper
        """
        if isinstance(item, Equipment):
            if item in self.items:
                self.items[self.items.index(item)] = None

    def is_full(self):
        """
        @summary dit si l'inventaire est plein
        @return : bool
        """
        return len(self.items) == self.max_size

    def append(self, item: Item):
        """
        @summary ajoute un element a l'inventaire
        @param  item : Item   item a ajouter a l'inventaire
        """
        self.items.append(item)
        if item.item_type == "weapon":
            print(item.item_type)
        elif item.item_type == "armor":
            print(item.item_type)
        elif item.item_type == "jewel":
            print(item.item_type)
        elif item.item_type == "consumable":
            print(item.item_type)
        elif item.item_type == "spellbook":
            print(item.item_type)
