"""
- Monsters are also characters
-  Your character has to Battle against them
- They can drop one or more objects when they die, plus an amount of gold, those you can add it to an Inventory.

"""
from src.perso.character import Character
from src.item import Item
from res.ressources_id import monsters_id
from typing import List
from random import randint


class Monster(Character):
    def __init__(self) -> None:
        super().__init__("Mechant")
        self.icon_id = randint(0, len(monsters_id)-1)

    def __str__(self) -> str:
        return "Monster type:{} | level :{}".format(self.icon_id, self.level)

    def level_up(self) -> None:
        super().level_up()
        self.armor += randint(1, self.level)

    def drop(self) -> List[Item]:
        """
        @summary when a mob die he loot drops
        @return : List[Item] une list de loot
        """
        if self.health <= 0:
            return [Item.random() for _ in range(randint(0, 3))]
        else:
            return []

