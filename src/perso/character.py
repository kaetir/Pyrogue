"""
- Your character has a name.
- He has stats such as:
·         Health point when it reaches 0, you die and start back on another generated carte,
                with no level, no equipment, gold and Inventory emptied
·         armor point that block a certain amount of damage and decreased after taking damages
·         Chance of dodge (%) to avoid attacks (damages are nullified)
·         Chance of parry (%) to reduce amount of damage by 70%
·         Chance of critical hit (%) to double the amount of damage inflicted
·         Magic Point (MP) to use spells
·         Damage minimum and maximum you can inflict on monsters
·         Armor point, reduced incoming damage by a percentage
·         Level, each leave increase a small of the characteristics above
·         Experience bar, when filled, increase current level by one

- Your character can earn experience to gain level after a won Battle. When you level up, his stats are raised, but
            existing monsters stats are raising too.

"""
from __future__ import annotations
from random import randint, random
from src.my_utils import fib_rec
from src.inventory import Inventory
#from src.item import Equipment

import math


class Character:
    def __init__(self, name: str = "billy"):
        """
        @summary Constructeur
        @param : str nom du personnage
        """
        self.name = name
        self.health: int = 20
        self.max_health: int = 20
        self.chance_of_dodge: float = 0.05
        self.chance_of_parry: float = 0.05
        self.chance_of_critical: float = 0.1
        self.mana: int = 10
        self.max_mana: int = 10
        self.damage_min: int = 1
        self.damage_max: int = 3
        self.armor: int = 0
        self.max_armor: int = 0
        self.level: int = 1
        self.experience: int = 0
        self.icon_id = 0

        # Utiles pour le personnage Principal
        self.orientation = 0  # % 4 : orientation du personnage dans la salle
        self.position = [0, 0]  # position du personnage sur la carte

        # INVENTAIRES
        self.inventory = Inventory()  # Rempli d'items

    def __str__(self) -> str:
        return self.name + " de niveau " + str(self.level)

    def set_pos(self, x, y):
        self.position = [x, y]

    def get_pos(self):
        return self.position

    def get_health(self):
        return self.health

    def get_mana(self):
        return self.mana

    def get_experience(self):
        return self.experience

    def get_armor(self):
        return self.armor

    def get_inventory(self):
        return self.inventory.items

    def get_life_percent(self):
        return self.health / self.max_health if self.max_health != 0 else 0

    def get_mana_percent(self):
        return self.mana / self.max_mana if self.max_mana != 0 else 0

    def get_experience_percent(self):
        return self.experience / (fib_rec(self.level) * 100)

    def get_armor_percent(self):
        return self.armor / self.max_armor if self.max_armor != 0 else 0

    def get_orientation(self):
        return self.orientation % 4

    def set_orientation(self, new_orient):
        self.orientation = new_orient % 4

    def collect(self, item):
        """
        @summary Recuperation d'un objet par le personnage
        @param item: objet a recuperer
        @return: false si l'inventaire est plein sinon true
        """
        if self.inventory.is_full():
            return False
        # Else
        self.inventory.append(item)
        return True

    def gain_xp(self, amount: int) -> None:
        """
        @summary Le perso viens faire une action qui lui rapporte de l'xp
        @summary On lui fait monter des nivreau si besoin et on lui ajoute le restant de l'xp
        @param : int nombre de points d'xp a donner au joueur
        """
        while self.experience + amount > fib_rec(self.level) * 100:
            amount -= fib_rec(self.level) * 100
            self.level_up()

        self.experience += amount

    def level_up(self) -> None:
        """
        @summary Level up du perso et boost des stats
        @summary capage des states de chances a 80% (en vrai ca peut dépasser mais osef)
        """
        print("### LEVEL UP {}###".format(self.level + 1))
        self.level += 1
        self.max_health += randint(1, self.level)
        self.health = self.max_health
        #self.max_armor += randint(1, self.level)
        self.armor = self.max_armor
        self.chance_of_dodge += random() / 10 if self.chance_of_dodge < 0.8 else 0.
        self.chance_of_parry += random() / 10 if self.chance_of_parry < 0.8 else 0
        self.chance_of_critical += random() / 3 if self.chance_of_parry < 0.8 else 0
        self.max_mana += randint(1, self.level)
        self.mana = self.max_mana
        self.damage_min += randint(1, self.level)
        self.damage_max += randint(1, self.level)

    def take_damage(self, amount: int) -> bool:
        """
        @summary fait prendre des dégats au joueur,
        @summary on calcul ses chances de dodge et de parry a partir de 2 nombres aléatoires
        @summary on déduit les dégats de parade
        @param : int le nombre de degat que le joueur va prendre
        @return si le joueur est vivant -> true = alive
        """
        if random() < self.chance_of_dodge:
            print(self.name + " dodged")
            return True
        if random() < self.chance_of_parry:
            print(self.name + " parry")
            if self.armor - math.ceil(amount * 0.3) > 0:
                self.armor, amount = self.armor - math.ceil(amount * 0.3), 0
            else:
                self.armor, amount = 0, math.ceil(amount * 0.3) - self.armor
            self.health -= (1 - self.armor) * amount
            return self.is_alive()
        print(self.name + " prend dans le cul")
        if self.armor - amount > 0:
            self.armor, amount = self.armor - amount, 0
        else:
            self.armor, amount = 0, amount - self.armor

        self.health -= (1 - self.armor) * amount
        return self.is_alive()

    def inflict_damage(self, other: Character, amount: int) -> None:
        """
        @summary fait prendre a un autre perso des dégats infligé par nous
        @summary on ne calcule pas les dégats ici parce qu'ils dépendent de si c'est un sort ou une attaque
        @param : Character l'autre perso a qui on veut en mettre sur le visage
        @param : int le nombre de dégats qu'on lui met sur le visage
        """
        if amount < self.damage_min:
            other.take_damage(self.damage_min)
        else:
            other.take_damage(amount)

    def print(self) -> None:
        """
        @summary Affiche un joli résumé formaté
        """
        print(self)
        print("HP :", self.health, " SP :", self.armor, "MP :", self.mana)

    def is_alive(self) -> bool:
        """
        @summary dit si le joueur et en vie
        @return booléen True = vivant
        """
        return self.health > 0

    def equip_spellbook(self, current_item, cursor) -> bool:
        return True

    def equip_consumable(self, current_item, cursor: int) -> bool:
        return True

    def equip(self, item: Equipment):
        self.inventory.equip(item)

        # recalcule de l'armure
        self.armor = 0
        if self.inventory.helmet is not None:
            self.armor += self.inventory.helmet.value
        if self.inventory.chest is not None:
            self.armor += self.inventory.chest.value
        if self.inventory.legs is not None:
            self.armor += self.inventory.legs.value
        if self.inventory.boots is not None:
            self.armor += self.inventory.boots.value
        if self.inventory.gloves is not None:
            self.armor += self.inventory.gloves.value
        if self.inventory.ring is not None:
            self.armor += self.inventory.ring.value
        if self.inventory.amulet is not None:
            self.armor += self.inventory.amulet.value
        self.max_armor = self.armor

        return True

    def buy(self, item: Item, merchant: Merchant):
        if self.inventory.money >= item.prix:
            merchant.inventory.items[merchant.inventory.items.index(item)] = None
            self.inventory.append(item)
            self.inventory.money -= item.prix

    def sell(self, item, merchant):
        pass

    def heal(self, amount: int)-> None:
        """
        @summary rend de la vie au perso
        @param amount: la quantité
        @return: None
        """
        if self.health + amount >= self.max_health:
            self.health = self.max_health
        else:
            self.health += amount
