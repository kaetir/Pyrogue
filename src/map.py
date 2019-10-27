"""
- Map has Rooms and are bound each other linearly,

"""

from math import floor
from random import random

import matplotlib.pyplot as plt
import numpy as np

from src.room import Room


class MapDungeon:
    map_size: int = 15
    x: int = 0
    y: int = 0
    rooms: list = []

    def __init__(self, size: int = 15) -> None:
        """
        @brief constructeur
        @param : int taille de la map
        """
        super().__init__()
        self.gen_map(size)

    def __str__(self) -> str:
        """
        @brief fonciton pour le retour string
        """
        return self.pts.__str__()

    def gen_map(self, size: int = 15) -> None:
        """
        @brief generateur de map aléatoire sur le model de l'algo du marcheur
        @param : int taille de la map
        """
        self.map_size = size
        x = self.x
        y = self.y
        pts = [[x, y]]

        while len(np.unique(np.array(pts), axis=0)) < self.map_size:
            eps = 2 * floor(2 * random()) - 1

            if random() < .5:
                x += eps
            else:
                y += eps

            pts += [[x, y]]

        idx: int
        for idx, val in enumerate(pts):
            self.rooms += [Room(val[0], val[1])]

    def disp_map(self, filename: str = None):
        """
        @brief affichage de la map et sauvegarde éventuelle
        @param : str fichier de sauvegarde de l'image
        """
        stp = np.array([x.get_pos() for x in self.rooms])

        # Desctivation des axes
        plt.axes(aspect='equal')
        plt.axis('off')

        # affichage des salles
        for rom in stp:
            plt.plot([rom[0] - 0.5, rom[0] - 0.5, rom[0] + 0.5, rom[0] + 0.5, rom[0] - 0.5],
                     [rom[1] - 0.5, rom[1] + 0.5, rom[1] + 0.5, rom[1] - 0.5, rom[1] - 0.5],
                     color="black", lw=4)
        # plt.scatter(stp[:, 0], stp[:, 1])

        # affichage des liaisons entre les salles
        plt.plot(stp[:, 0], stp[:, 1])

        # affichage des liens entres les salles
        plt.scatter(stp[0, 0], stp[0, 1], color='r', lw=4)  # entrée
        plt.scatter(stp[-1, 0], stp[-1, 1], color='y', lw=4)  # sortie

        # sauvegarde du graph
        if filename is not None:
            plt.savefig(filename, transparent=True)

        # affichage du graph
        plt.show()
