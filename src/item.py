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

    swordDamage = {
        10: 3,
        11: 3,
        13: 3,
        12: 3,
        14: 3,
        15: 3,
        16: 3,
        17: 6,
        20: 3,
        21: 3,
        22: 3,
        24: 3,
        23: 3,
        25: 3,
        26: 3,
        27: 6,
        30: 3,
        31: 3,
        32: 3,
        33: 3,
        34: 6,
        35: 8,
        36: 3,
        37: 3,
        78: 15
    }

    def __init__(self, type_equip: str = None) -> None:
        super().__init__()
        if type_equip is None:
            self.equipment_type = choice(self.static_equipment_type)
        else:
            if type_equip in self.static_equipment_type:
                self.equipment_type = type_equip
            else:
                self.equipment_type = choice(self.static_equipment_type)

        self.random_icon()

        if self.equipment_type == "weapon":
            self.prix = self.swordDamage[self.icon_id] * 100
            # 5% chance of parry
            self.block_chance = 0.05
            self.damage = self.swordDamage[self.icon_id]
        else:
            self.prix = 100
            self.damage = 1
            # 30% chance of parry
            self.block_chance = 0.3

        self.precision = 0.95

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
        self.prix = 1
        self.value = 1
        self.random_equipement()

    def random_equipement(self):
        if self.equipment_type == "helmet":
            self.icon_id = choice(items_id["helmets"])
            self.value = 2
            self.prix = randint(150, 200)
        elif self.equipment_type == "chest":
            self.icon_id = choice(items_id["chests"])
            self.value = 5
            self.prix = randint(500, 1000)
        elif self.equipment_type == "legs":
            self.icon_id = choice(items_id["legs"])
            self.value = 3
            self.prix = randint(300, 500)
        elif self.equipment_type == "boots":
            self.icon_id = choice(items_id["boots"])
            self.value = 2
            self.prix = randint(50, 100)
        elif self.equipment_type == "gloves":
            self.icon_id = choice(items_id["gloves"])
            self.value = 2
            self.prix = randint(50, 100)
        elif self.equipment_type == "amulet":
            self.icon_id = choice(items_id["amulets"])
            self.value = 1
            self.prix = randint(50, 100)
        elif self.equipment_type == "ring":
            self.icon_id = choice(items_id["rings"])
            self.value = 1
            self.prix = randint(50, 100)


class Consumables(Item):
    item_type = "consumable"
    bonus: bool = True

    def __init__(self):
        super().__init__()
        self.icon_id = choice(items_id["sandwichs"])

    def use(self, c: Character) -> None:
        if self.bonus:
            c.heal(c.max_health // 2)
            c.mana += 3 if c.mana + 3 <= c.max_mana else c.max_mana - c.mana

        print("Yummmy !!!!🥪")


class SpellBook(Item):
    item_type = "spellbook"
    bonus: bool = False
    # TODO TROUVER UNE VALEUR CORRECTE
    prix = randint(10, 100)

    IsBonus = {
        70: False,  # poison
        71: False,  # boom
        72: False,  # skip
        73: True,  # armorBoost
        74: True,  # heal
        75: True  # vol a la tire
    }
    costs = {
        70: 1,  # poison
        71: 1,  # boom
        72: 0,  # skip
        73: 5,  # armorBoost
        74: 2,  # heal
        75: 1  # vol a la tire
    }

    def __init__(self):
        super().__init__()
        self.random_spellbook()
        self.cost = self.costs[self.icon_id]
        self.bonus = self.IsBonus[self.icon_id]

    def use(self, source: Character, destination: Monster) -> bool:
        """
        @summary utilise un spell de la source sur la destination si c'est un monstre et que le sort est un debuff
        @param source: le joueur qui lance le sort
        @param destination: le mob qui prend cher
        @return: si le sort a pu etre lancé
        """
        if self.cost > source.mana:
            return False
        if self.icon_id != 71:
            source.mana -= self.cost

        if self.bonus:
            # heal
            if self.icon_id == 74:
                source.health = source.max_health
            # shield
            elif self.icon_id == 73:
                source.armor += 5
            # vol a la tire
            elif self.icon_id == 75:
                source.inventory.money += randint(50, 100)
                destination.take_damage(destination.max_health // 5)
            print("mathémagie BONUS", self.icon_id)
            print("{} use a spell on himself".format(source.name))
        else:
            # TODO states -> poison
            if self.icon_id == 70:
                destination.take_damage(destination.max_health // 3)
            # Boom == INSTAKILL
            if self.icon_id == 71:
                source.mana = 0
                destination.health = 0
            # TODO skip turn
            if self.icon_id == 72:
                print("POUF")
            print("mathémagie MALLUS", self.icon_id)
            print("{} use a spell on {}".format(self.name, destination.name))
        return True

    def random_spellbook(self):
        self.icon_id = choice(items_id["spellbooks"])
