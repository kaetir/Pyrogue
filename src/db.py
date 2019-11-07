import json
from perso.character import Character
from pymongo import MongoClient
from pymongo.errors import *
from uuid import getnode as get_mac


def get_mac_hex() -> hex:
    """
    @return: hex
    """
    return hex(get_mac())


class PyrogueDB:

    def __init__(self) -> None:
        """
        @summary connecteur db distante mongo
        """
        self.client = MongoClient('trustme.ovh', 27017)
        self.db = self.client['pyrogue']

    def save(self, carte: str, player: Character) -> int:
        try:
            save_table = self.db["saves"]
            jason = {"identity": get_mac_hex(),
                     "character": player,
                     "map": carte,
                     "achievement": ["TODO"]
                     }

            save_table.delete_many({"identity": get_mac_hex()})
            save_table.insert_one(jason)

        except ConnectionFailure:
            return 1
        except CursorNotFound:
            return 2
        return 0

    def load(self) -> int:
        try:
            save_table = self.db["saves"]

            for s in save_table.find({"identity": get_mac_hex()}):
                print(s)

        except ConnectionFailure:
            return 1
        except CursorNotFound:
            return 2
        return 0


if __name__ == '__main__':
    my = PyrogueDB()
    my.save("map", "toitoine")

    my.load()
