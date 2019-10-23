"""
    -   containing
        - characters, such as monsters to battle, real persons to interact with,
        - find objects,
        - or nothing happen while crossing rooms.

"""


class Room:
    x: int = 0
    y: int = 0
    inside = "du caca dans la salle"
    # left, top, right, bottom
    door = [0, 0, 0, 0]
    discovered: bool = False

    def __init__(self, x, y) -> None:
        """
        @brief constructeur
        @param x : int position de la room
        @param y : int position de la room
        """
        super().__init__()
        self.x = x
        self.y = y

    def __str__(self) -> str:
        print("pos :", self.x, self.y, "\n", self.inside)

    def get_pos(self) -> (int, int):
        """
        @brief retourne les pos de la salle
        @return : [int, int] x et y
        """
        return self.x, self.y

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
