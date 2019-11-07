"""
- You can sell object and buy new objects to a merchant that you can encounter in the carte
- Merchant are characters
- Merchant have an Inventory, which permits to store objects you can buy or sell objects.


"""
import random
from src.perso.character import Character
from src.ressources_id import merchants_id


class Merchant(Character):
    def __init__(self) -> None:
        super().__init__("Merchant")
        print("Bonjour, tu en veux c'est de la bonne")
        self.icon_id = random.randint(0, len(merchants_id)-1)
