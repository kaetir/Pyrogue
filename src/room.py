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
        super().__init__()
        self.x = x
        self.y = y

    def __str__(self) -> str:
        print("pos :", self.x, self.y, "\n", self.inside)

    def get_pos(self):
        return self.x, self.y

    def is_discovered(self):
        return self.discovered

    def discover(self):
        self.discovered = True
