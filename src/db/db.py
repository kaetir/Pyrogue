from __future__ import annotations

import json
from pymongo import MongoClient
from pymongo.errors import *
from uuid import getnode as get_mac
import pickle
import threading


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

        try:
            self.saves_table = self.db["saves"]
            self.players_table = self.db["players"]
            self.fights_table = self.db["fights"]

        except ConnectionFailure:
            print("ConnectionFailure")

    def save_stats_and_achievement(self, player: Character):
        # TODO
        try:
            for p in self.players_table.find({"identity": get_mac_hex()}):
                print(p)
                if p["identity"] == get_mac_hex():
                    achievements = p["achievement"]
                    stats = p["stats"]
                    for achiev in achievements:
                        print(achiev)
                    for stat in stats:
                        print(stat)

        except ConnectionFailure:
            return 1
        except CursorNotFound:
            return 2
        return 0

    def save(self, game) -> int:
        try:
            jason = {"identity": get_mac_hex(),
                     "player": pickle.dumps(game.character),
                     "map": pickle.dumps(game.map),
                     "actual_level": game.actual_level
                     }

            self.saves_table.delete_many({"identity": get_mac_hex()})
            self.saves_table.insert_one(jason)

        except ConnectionFailure:
            return 1
        except CursorNotFound:
            return 2
        return 0

    def save_fight(self, player: Character, mob: Monster, coups: [coup]) -> int:
        try:
            jason = {
                "character": pickle.dumps(player),
                "mob": pickle.dumps(mob),
                "coups": pickle.dumps(coups)
            }
            # threading for no slowing
            download_thread = threading.Thread(target=self.fights_table.insert_one, args=[jason])
            download_thread.start()

        except ConnectionFailure:
            return 1
        except CursorNotFound:
            return 2
        print("fight saved")
        return 0

    def load(self) -> Optional[int, [Any]]:
        try:
            for s in self.saves_table.find({"identity": get_mac_hex()}):
                return pickle.loads(s["player"]), pickle.loads(s["map"]), s["actual_level"]
        except ConnectionFailure:
            return 1
        except CursorNotFound:
            return 2
        return 0


if __name__ == '__main__':
    my = PyrogueDB()
    # my.save("map", "toitoine")
    # my.save_stats_and_achievement("moi")

    my.load()

    for f in my.fights_table.find({}):
        print(pickle.loads(f["character"]))
        print(pickle.loads(f["mob"]))
        [print(str(c)) for c in pickle.loads(f["coups"])]
        print("================================")
