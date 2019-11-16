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
#from src.perso.character import Character


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
        11: 12,
        13: 5,
        12: 7,
        14: 6,
        15: 12,
        16: 10,
        17: 20,
        20: 4,
        21: 5,
        22: 6,
        24: 7,
        23: 8,
        25: 9,
        26: 16,
        27: 18,
        30: 13,
        31: 17,
        32: 11,
        33: 17,
        34: 16,
        35: 10,
        36: 2,
        37: 3,
        78: 30
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

    values = {
        "helmets": {
            40: 6,
            45: 1,
            50: 4,
            55: 2,
            60: 5,
            65: 3
        },
        "chests": {
            41: 12,
            46: 2,
            51: 8,
            56: 4,
            61: 10,
            66: 6
        },
        "legs": {
            42: 9,
            47: 2,
            52: 7,
            57: 6,
            62: 8,
            67: 4
        },
        "boots": {
            43: 6,
            48: 2,
            53: 4,
            58: 2,
            63: 5,
            68: 3
        },
        "gloves": {
            44: 6,
            49: 1,
            54: 4,
            59: 2,
            64: 5,
            69: 3
        },
        "rings": {
            93: 1,
            94: 1,
            95: 1
        },
        "amulets": {
            18: 1,
            19: 1
        }
    }

    def __init__(self) -> None:
        super().__init__()
        self.equipment_type = choice(self.static_equipment_type)
        self.prix = 1
        self.value = 1
        self.random_equipement()

    def random_equipement(self):
        if self.equipment_type not in ["legs", "boots", "gloves"]:
            self.icon_id = choice(items_id[self.equipment_type + "s"])
            self.value = self.values[self.equipment_type + "s"][self.icon_id]
        else:
            # nique la gramaire
            self.icon_id = choice(items_id[self.equipment_type])
            self.value = self.values[self.equipment_type][self.icon_id]
        self.prix = self.value * 100 + randint(-int(self.value * 20), int(self.value * 20))


class Consumables(Item):
    item_type = "consumable"
    bonus: bool = True

    def __init__(self):
        super().__init__()
        self.icon_id = choice(items_id["sandwichs"])

    def use(self, c) -> None:
        if self.bonus:
            c.heal(c.max_health // 2)
            c.mana += 3 if c.mana + 3 <= c.max_mana else c.max_mana - c.mana

        print("Yummmy !!!!🥪")


class SpellBook(Item):
    item_type = "spellbook"
    bonus: bool = False

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

    costsGold = {
        70: [150, 300],  # poison
        71: [300, 1000],  # boom
        72: [1, 1],  # skip
        73: [100, 200],  # armorBoost
        74: [200, 400],  # heal
        75: [200, 400]  # vol a la tire
    }

    def __init__(self):
        super().__init__()
        self.random_spellbook()
        self.cost = self.costs[self.icon_id]
        self.bonus = self.IsBonus[self.icon_id]
        self.prix = randint(self.costsGold[self.icon_id][0], self.costsGold[self.icon_id][1])

    def use(self, source, destination) -> bool:
        """
        @summary utilise un spell de la source sur la destination si c'est un monstre et que le sort est un debuff
        @param source: le joueur qui lance le sort
        @param destination: le mob qui prend cher
        @return: si le sort a pu etre lancé
        """
        if self.cost > source.mana:
            return False
        source.mana -= self.cost

        if self.bonus:
            # heal
            if self.icon_id == 74:
                source.health = source.max_health
            # shield
            elif self.icon_id == 73:
                source.armor += source.level * 2
            # vol a la tire
            elif self.icon_id == 75:
                source.inventory.money += randint(25, 50)
                destination.take_damage(destination.max_health // 5)
            print("mathémagie BONUS", self.icon_id)
            print("{} use a spell on himself".format(source.name))
        else:
            # TODO states -> poison
            if self.icon_id == 70:
                destination.take_damage(destination.max_health // 3)
            # Boom == massdamage
            if self.icon_id == 71:
                destination.health -= source.mana * 3
                source.mana = 0
            # TODO skip turn
            if self.icon_id == 72:
                print("POUF")
            print("mathémagie MALLUS", self.icon_id)
            print("{} use a spell on {}".format(self.name, destination.name))

        return True

    def random_spellbook(self):
        self.icon_id = choice(items_id["spellbooks"])
