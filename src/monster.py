"""
- Monsters are also characters
-  Your character has to battle against them
- They can drop one or more objects when they die, plus an amount of gold, those you can add it to an Inventory.

"""
import src.character as Character
import src.item as Item
from typing import List
from random import randint


class Monster(Character):
    def __init__(self) -> None:
        super().__init__("Mechant")
        print("Booohhh")

    def __str__(self) -> str:
        return "boooooo"

    def drop(self) -> List[Item]:
        """
        @brief when a mob die he loot drops
        @return : List[Item] une list de loot
        """
        if self.health <= 0:
            return [Item.random() for _ in range(randint(0, 3))]
        else:
            return []

