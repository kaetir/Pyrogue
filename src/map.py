"""
- Map has Rooms and are bound each other linearly,
    -   containing
        - characters, such as monsters to battle, real persons to interact with,
        - find objects,
        - or nothing happen while crossing rooms.
"""

from math import floor
from random import random

import numpy as np
import matplotlib.pyplot as plt


class MapDungeon:
    map_size: int = 15
    x: int = 0
    y: int = 0
    pts = [[x, y]]


    def __init__(self) -> None:
        super().__init__()
        self.gen_map()

    def __str__(self) -> str:
        return self.pts.__str__()

    def gen_map(self, size: int = 15) -> np.array:
        self.map_size = size

        while len(np.unique(np.array(self.pts), axis=0)) < self.map_size:
            #for i in range(size):
            eps = 2 * floor(2 * random()) - 1

            if random() < .5:
                self.x += eps
            else:
                self.y += eps

            self.pts += [[self.x, self.y]]
            print(self.pts)

        return  self.pts

    def disp_map(self):
        stp = np.array(self.pts)

        plt.scatter(stp[:, 0], stp[:, 1])
        plt.plot(stp[:, 0], stp[:, 1])
        plt.scatter(stp[0, 0], stp[0, 1], color='r')
        plt.scatter(stp[-1, 0], stp[-1, 1], color='y')
        plt.show()
