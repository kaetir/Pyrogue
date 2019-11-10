"""
- You can sell object and buy new objects to a merchant that you can encounter in the carte
- Merchant are characters
- Merchant have an Inventory, which permits to store objects you can buy or sell objects.


"""
from src.perso.character import Character
from res.ressources_id import merchants_id
from src.item import *


class Merchant(Character):
    def __init__(self) -> None:
        super().__init__("Merchant")
        # print("Bonjour, tu en veux c'est de la bonne")
        self.icon_id = randint(0, len(merchants_id) - 1)
        for i in range(3):
            self.inventory.append(Consumables())
        for i in range(3):
            self.inventory.append(Armor())
        for i in range(3):
            self.inventory.append(Weapon())
