"""
- Monsters are also characters
-  Your character has to battle against them
- They can drop one or more objects when they die, plus an amount of gold, those you can add it to an Inventory.

"""
import Character
import Item
from typing import List
from random import randint


class Monster(Character):
    def __init__(self):
        super.__init__()

    def __str__(self):
        super.__str__()

    def drop(self) -> List[Item]:
        """
        @brief when a mob die he loot drops
        @return : List[Item] une list de loot
        """
        return [Item.random() for _ in range(randint(0, 3))]
