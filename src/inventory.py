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
from src.item import *
from src.perso.character import *


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

    def equip(self, item: Equipment):
        """
        @summary equipe un objet et l'enleve de l'inventaire si il est dedans
        @param item: item a equiper
        @return bool: code d'erreur
        """
        if isinstance(item, Equipment):
            if item in self.items:
                if isinstance(item, Armor):
                    if item.armor_type == "helmet":
                        self.helmet, self.items[self.items.index(item)] = \
                            self.items[self.items.index(item)], self.helmet
                elif isinstance(item, Weapon):
                    self.weapon, self.items[self.items.index(item)] = \
                        self.items[self.items.index(item)], self.weapon

        else:
            return 1

        # recalcule de l'armure dans le player

    def use(self, cons: Consumables, car: Character):
        if cons in self.items:
            self.items[self.items.index(cons)] = None
            cons.use(car)
        return 0

    def throw(self, item: Item) -> bool:
        if item in self.items:
            self.items[self.items.index(item)] = None
        return 0

    def is_full(self):
        """
        @summary dit si l'inventaire est plein
        @return : bool
        """
        i = 0
        while i < self.max_size:
            i += 1
            if self.items[i] is None :
                return False
        return True

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
            self.active_comsumable[pos], self.items[self.items.index(c)] = c, self.active_comsumable[pos]
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
            self.active_spells[pos], self.items[self.items.index(sb)] = sb, self.active_spells[pos]
            return 0
        return 1
