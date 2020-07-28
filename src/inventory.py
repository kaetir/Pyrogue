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

from __future__ import annotations
from perso.character import *
from item import *


class Inventory:

    def __init__(self) -> None:
        super().__init__()

        # Rempli d'items
        self.max_size: int = 6 * 8
        self.items: list[Optional[Item, None]] = [None] * self.max_size

        # les consumables sont stoké
        # max size 4
        self.active_comsumable: list[Optional[Consumables, None]] = [None, None, None, None]

        # Les speels sont tous dans des speels book et on en actives certain
        # max size 3
        self.active_spells: list[Optional[SpellBook, None]] = [None, None, None]

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

    def __getitem__(self, item: Item) -> Optional[Item, None]:
        """
        @summary surcharge de [] pour recherché un item
        @return: Item
        """
        if item in self.items:
            return self.items[self.items.index(item)]
        else:
            return None

    def __setitem__(self, item: Item, value: Optional[Item, None]) -> None:
        """
        @summary surcharge de [] pour set un item
        @return: Item
        """
        if item in self.items:
            self.items[self.items.index(item)] = value

    def equip(self, item: Equipment):
        """
        @summary equipe un objet et l'enleve de l'inventaire si il est dedans
        @param item: item a equiper
        @return bool: code d'erreur
        """
        if item in self.items:
            if item.equipment_type == "helmet":
                self.helmet, self[item] = item, self.helmet
            elif item.equipment_type == "chest":
                self.chest, self[item] = item, self.chest
            elif item.equipment_type == "legs":
                self.legs, self[item] = item, self.legs
            elif item.equipment_type == "boots":
                self.boots, self[item] = item, self.boots
            elif item.equipment_type == "gloves":
                self.gloves, self[item] = item, self.gloves
            elif item.equipment_type == "amulet":
                self.amulet, self[item] = item, self.amulet
            elif item.equipment_type == "ring":
                self.ring, self[item] = item, self.ring
            elif item.equipment_type == "weapon":
                self.weapon, self[item] = item, self.weapon
            elif item.equipment_type == "shield":
                self.shield, self[item] = item, self.shield
            else:
                return 0
        return 1

        # recalcule de l'armure dans le player

    def use(self, cons: Consumables, car: Character):
        """
        @summary fait usage d'un consomable sur un personnage
        @param cons:
        @param car:
        @return:
        """
        if cons in self.items:
            self[cons] = None
            cons.use(car)
        return 0

    def throw(self, item: Item) -> bool:
        """
        @summary jete un item en le retirant de l'inventaire
        @param item: l'item a jeter
        @return: bool : True si l'item a été trouvé et jeté
        """
        if item in self.items:
            self[item] = None
            return True
        return False

    def is_full(self):
        """
        @summary dit si l'inventaire est plein
        @return : bool
        """
        return None not in self.items

    def append(self, item: Item):
        """
        @summary ajoute un element a l'inventaire
        @param  item : Item   item a ajouter a l'inventaire
        """
        if not self.is_full():
            i = 0
            while self.items[i] is not None:
                i += 1
            self.items[i] = item

    def equip_consumable(self, c: Consumables, pos: int):
        """
        @summary : equipe un consumable de l'inventaire vers la barre active
        @param c: le consumable a équiper
        @param pos: la pos dans la barre des équipable
        @return:
        """
        if c in self.items:
            self.active_comsumable[pos], self[c] = c, self.active_comsumable[pos]
            return 0
        return 1

    def equip_spellbook(self, sb: SpellBook, pos: int):
        """
        @summary
        @param sb: le spellbook a équiper
        @param pos: la pos dans la barre des équipable
        @return:
        """
        if sb in self.items:
            self.active_spells[pos], self[sb] = sb, self.active_spells[pos]
            return 0
        return 1
