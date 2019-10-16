"""
- Your character has a name.
- He has stats such as:
·         Health point when it reaches 0, you die and start back on another generated map, with no level, no equipment, gold and Inventory emptied
·         Shield point that block a certain amount of damage and decreased after taking damages
·         Chance of dodge (%) to avoid attacks (damages are nullified)
·         Chance of parry (%) to reduce amount of damage by 70%
·         Chance of critical hit (%) to double the amount of damage inflicted
·         Magic Point (MP) to use spells
·         Damage minimum and maximum you can inflict on monsters
·         Armor point, reduced incoming damage by a percentage
·         Level, each leave increase a small of the characteristics above
·         Experience bar, when filled, increase current level by one

- Your character can earn experience to gain level after a won battle. When you level up, his stats are raised, but existing monsters stats are raising too.

"""
from utils import fibRec
from random import randint, random
import math


class Character:
    Name = "billy"
    Health = 20
    Shield = 10
    ChanceOfDodge = 0.05
    ChanceOfParry = 0.05
    ChanceOfCritical = 0.1
    MP = 10
    DamageMin = 1
    DamageMax = 10000000
    Armor = 0.1
    Level = 1
    Experience = 0

    def __init__(self, name="billy"):
        """
        @brief Constructeur
        @param : str nom du personnage
        """
        self.Name = name

    def __str__(self) -> str:
        return self.Name + " de niveau " + str(self.Level)

    def gain_xp(self, amount: int) -> None:
        """
        @brief Le perso viens faire une action qui lui rapporte de l'xp
        @brief On lui fait monter des nivreau si besoin et on lui ajoute le restant de l'xp
        @param : int nombre de points d'xp a donner au joueur
        """
        while self.Experience + amount > fibRec(self.Level) * 100:
            amount -= fibRec(self.Level) * 100
            self.level_up()

        self.Experience += amount

    def level_up(self) -> None:
        """
        @brief Level up du perso et boost des stats
        @brief capage des states de chances a 80% (en vrai ca peut dépasser mais osef)
        """
        print("### LEVEL UP {}###".format(self.Level+1))
        self.Level += 1
        self.Health += randint(1, self.Level)
        self.Shield += randint(1, self.Level)
        self.ChanceOfDodge += self.ChanceOfDodge < 0.8 if random() / 10 else 0
        self.ChanceOfParry += self.ChanceOfParry < 0.8 if random() / 10 else 0
        self.ChanceOfCritical += self.ChanceOfParry < 0.8 if random() / 3 else 0
        self.MP += randint(1, self.Level)
        self.DamageMin += randint(1, self.Level)

    def take_damage(self, amount: int) -> bool:
        """
        @brief fait prendre des dégats au joueur,
        @brief on calcul ses chances de dodge et de parry a partir de 2 nombres aléatoires
        @brief on déduit les dégats de parade
        @param : int le nombre de degat que le joueur va prendre
        @return si le joueur est vivant -> true = alive
        """
        if random() < self.ChanceOfDodge:
            return True
        if random() < self.ChanceOfParry:
            if self.Shield - math.ceil(amount * 0.3) > 0:
                self.Shield, amount = self.Shield - math.ceil(amount * 0.3), 0
            else:
                self.Shield, amount = 0, math.ceil(amount * 0.3) - self.Shield
            self.Health -= (1 - self.Armor) * amount
            return self.is_alive()

        if self.Shield - amount > 0:
            self.Shield, amount = self.Shield - amount, 0
        else:
            self.Shield, amount = 0, amount - self.Shield

        self.Health -= (1 - self.Armor) * amount
        return self.is_alive()

    def inflict_damage(self, other:Character, amount: int) -> None:
        """
        @brief fait prendre a un autre perso des dégats infligé par nous
        @brief on ne calcule pas les dégats ici parce qu'ils dépendent de si c'est un sort ou une attaque
        @param : Character l'autre perso a qui on veut en mettre sur le visage
        @param : int le nombre de dégats qu'on lui met sur le visage
        """
        if amount < self.DamageMin:
            other.take_damage(self.DamageMin)
        elif amount > self.DamageMax:
            other.take_damage(self.DamageMax)
        else:
            other.take_damage(amount)



    def print(self):
        """
        @brief Affiche un joli résumé formaté
        """
        print(self)
        print("HP :", self.Health, " SP :" , self.Shield, "MP :", self.MP )

    def is_alive(self) -> bool:
        """
        @brief dit si le joueur et en vie
        @return booléen True = vivant
        """
        return self.Health > 0
