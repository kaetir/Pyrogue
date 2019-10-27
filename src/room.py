"""
    -   containing
        - characters, such as monsters to battle, real persons to interact with,
        - find objects,
        - or nothing happen while crossing rooms.

"""
from __future__ import annotations

top = 0
right = 1
bottom = 2
left = 3

class Room:
    x: int = 0
    y: int = 0
    inside = "du caca dans la salle"
    # top, right, bottom, left
    doors = [0, 0, 0, 0]
    discovered: bool = False

    def __init__(self, x: int, y: int, doors=None):
        """
        @brief constructeur
        @param x : int position de la room
        @param y : int position de la room
        """
        super().__init__()
        if doors is None:
            doors = [0, 0, 0, 0]
        self.x = x
        self.y = y
        if doors is None:
            self.doors = [0, 0, 0, 0]
        else:
            self.doors = doors

    def __repr__(self) -> str:
        return "Room %d : %d" % (self.x, self.y)

    def __str__(self) -> str:
        return "pos :" + str(self.x) + " " + str(self.y) + "\n" + self.inside

    def get_pos(self) -> (int, int):
        """
        @brief retourne les pos de la salle
        @return : [int, int] x et y
        """
        return self.x, self.y

    def set_porte(self, p: int) -> None:
        """
        @brief retourne les pos de la salle
        @param le numéro de la porte a ouvrir
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
