"""
    -   containing
        - characters, such as monsters to Battle, real persons to interact with,
        - find objects,
        - or nothing happen while crossing rooms.

"""
from __future__ import annotations

import random
from src.perso.monster import Monster

class Room:
    # ne pas toucher
    top: int = 0
    right: int = 1
    bottom: int = 2
    left: int = 3

    def __init__(self, x: int, y: int, doors=None):
        """
        @brief constructeur
        @param x : int position de la room
        @param y : int position de la room
        @param doors : list(int) les portes
        """
        super().__init__()
        # top, right, bottom, left
        if doors is None:
            self.doors = [0, 0, 0, 0]
        else:
            self.doors = doors
        self.x = x
        self.y = y
        self.discovered: bool = False
        self.exit: bool = False
        self.enemy: Monster = None if random.randint(0, 1) < 0.7 else Monster()

    def __repr__(self) -> str:
        return "Room %d : %d" % (self.x, self.y)

    def __str__(self) -> str:
        return "pos :" + str(self.x) + " " + str(self.y) + "\n"

    def get_doors(self):
        return self.doors

    def set_exit(self):
        """
        @brief La salle devient une sortie
        """
        self.exit = True

    def is_exit(self):
        """
        @brief Demande  si la salle est une sortie
        @return : bool
        """
        return self.exit

    def get_pos(self) -> (int, int):
        """
        @brief retourne les pos de la salle
        @return : [int, int] x et y
        """
        return self.x, self.y

    def set_porte(self, p: int) -> None:
        """
        @brief assigne une porte a la salle
        @param p: le numéro de la porte a ouvrir
        """
        self.doors[p] = 1

    def is_discovered(self) -> bool:
        """
        @brief retourne si la salle est découverte
        @return : bool
        """
        return self.discovered

    def discover(self) -> None:
        """
        @brief rend une salle visible
        """
        self.discovered = True
