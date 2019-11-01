"""
- You can sell object and buy new objects to a merchant that you can encounter in the map
- Merchant are characters
- Merchant have an Inventory, which permits to store objects you can buy or sell objects.


"""
from src.perso.character import Character


class Merchant(Character):
    def __init__(self) -> None:
        super().__init__("Merchant")
        print("Bonjour, tu en veux c'est de la bonne")
