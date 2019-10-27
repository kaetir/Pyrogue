"""
- Your character has a name.
- He has stats such as:
·         Health point when it reaches 0, you die and start back on another generated map,
                with no level, no equipment, gold and Inventory emptied
·         Shield point that block a certain amount of damage and decreased after taking damages
·         Chance of dodge (%) to avoid attacks (damages are nullified)
·         Chance of parry (%) to reduce amount of damage by 70%
·         Chance of critical hit (%) to double the amount of damage inflicted
·         Magic Point (MP) to use spells
·         Damage minimum and maximum you can inflict on monsters
·         Armor point, reduced incoming damage by a percentage
·         Level, each leave increase a small of the characteristics above
·         Experience bar, when filled, increase current level by one

- Your character can earn experience to gain level after a won battle. When you level up, his stats are raised, but
            existing monsters stats are raising too.

"""
from __future__ import annotations
from random import randint, random
from src.my_utils import fib_rec

import math


class Character:
    name: str = "billy"
    health: int = 20
    max_health: int = 20
    shield: int = 10
    chance_of_dodge: float = 0.05
    chance_of_parry: float = 0.05
    chance_of_critical: float = 0.1
    mana: int = 10
    max_mana: int = 10
    damage_min: int = 1
    damage_max: int = 10000000
    armor: float = 0.1
    max_armor: float = 0.1
    level: int = 1
    experience: int = 0
    # Utiles pour le personnage Principal
    orientation: int = 0  # % 4 : orientation du personnage dans la salle
    position = [0, 0]  # position du personnage sur la map

    def __init__(self, name: str = "billy"):
        """
        @brief Constructeur
        @param : str nom du personnage
        """
        self.name = name

    def __str__(self) -> str:
        return self.name + " de niveau " + str(self.level)

    def set_pos(self, x, y):
        self.position = [x, y]

    def get_pos(self):
        return self.position

    def get_life_percent(self):
        return self.health / self.max_health

    def get_mana_percent(self):
        return self.mana / self.max_mana

    def get_armor_percent(self):
        return self.armor / self.max_armor

    def get_orientation(self):
        return self.orientation

    def set_orientation(self, new_orient):
        self.orientation = new_orient % 4

    def gain_xp(self, amount: int) -> None:
        """
        @brief Le perso viens faire une action qui lui rapporte de l'xp
        @brief On lui fait monter des nivreau si besoin et on lui ajoute le restant de l'xp
        @param : int nombre de points d'xp a donner au joueur
        """
        while self.experience + amount > fib_rec(self.level) * 100:
            amount -= fib_rec(self.level) * 100
            self.level_up()

        self.experience += amount

    def level_up(self) -> None:
        """
        @brief Level up du perso et boost des stats
        @brief capage des states de chances a 80% (en vrai ca peut dépasser mais osef)
        """
        print("### LEVEL UP {}###".format(self.level + 1))
        self.level += 1
        self.health += randint(1, self.level)
        self.shield += randint(1, self.level)
        self.chance_of_dodge += random() / 10 if self.chance_of_dodge < 0.8 else 0.
        self.chance_of_parry += random() / 10 if self.chance_of_parry < 0.8 else 0
        self.chance_of_critical += random() / 3 if self.chance_of_parry < 0.8 else 0
        self.mana_points += randint(1, self.level)
        self.damage_min += randint(1, self.level)

    def take_damage(self, amount: int) -> bool:
        """
        @brief fait prendre des dégats au joueur,
        @brief on calcul ses chances de dodge et de parry a partir de 2 nombres aléatoires
        @brief on déduit les dégats de parade
        @param : int le nombre de degat que le joueur va prendre
        @return si le joueur est vivant -> true = alive
        """
        if random() < self.chance_of_dodge:
            print(self.name + " dodged")
            return True
        if random() < self.chance_of_parry:
            print(self.name + " parry")
            if self.shield - math.ceil(amount * 0.3) > 0:
                self.shield, amount = self.shield - math.ceil(amount * 0.3), 0
            else:
                self.shield, amount = 0, math.ceil(amount * 0.3) - self.shield
            self.health -= (1 - self.armor) * amount
            return self.is_alive()
        print(self.name + " prend dans le cul")
        if self.shield - amount > 0:
            self.shield, amount = self.shield - amount, 0
        else:
            self.shield, amount = 0, amount - self.shield

        self.health -= (1 - self.armor) * amount
        return self.is_alive()

    def inflict_damage(self, other: Character, amount: int) -> None:
        """
        @brief fait prendre a un autre perso des dégats infligé par nous
        @brief on ne calcule pas les dégats ici parce qu'ils dépendent de si c'est un sort ou une attaque
        @param : Character l'autre perso a qui on veut en mettre sur le visage
        @param : int le nombre de dégats qu'on lui met sur le visage
        """
        if amount < self.damage_min:
            other.take_damage(self.damage_min)
        elif amount > self.damage_max:
            other.take_damage(self.damage_max)
        else:
            other.take_damage(amount)

    def print(self) -> None:
        """
        @brief Affiche un joli résumé formaté
        """
        print(self)
        print("HP :", self.health, " SP :", self.shield, "MP :", self.mana_points)

    def is_alive(self) -> bool:
        """
        @brief dit si le joueur et en vie
        @return booléen True = vivant
        """
        return self.health > 0
