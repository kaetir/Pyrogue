"""
- Map has Rooms and are bound each other linearly,

"""

from math import floor
from random import random

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np

from src.room import Room


class MapDungeon:
    def __init__(self, size: int = 15) -> None:
        """
        @brief constructeur
        @param : int taille de la map
        """
        super().__init__()
        self.rooms = []
        self.map_size = size
        self.gen_map(size)

    def __str__(self) -> str:
        """
        @brief fonciton pour le retour string
        """
        return self.rooms.__str__()

    def get_room(self, x, y):
        """
        @brief renvoie une room en fonction de ses coordonnées
        @param x : pos de la case
        @param y : pos de la case
        @return : Room
        """
        for r in self.rooms:
            if (x, y) == r.get_pos():
                return r
        return None  # Erreur Salle inexistante

    def gen_map(self, size: int = 15) -> None:
        """
        @brief generateur de map aléatoire sur le model de l'algo du marcheur
        @param : int taille de la map
        """
        self.map_size = size
        x = 0
        y = 0
        pts = [[x, y, [0, 0, 0, 0]]]

        while len(pts) < self.map_size:
            eps = 2 * floor(2 * random()) - 1

            olx = x  # Anciennes positions
            oly = y

            if random() < .5:
                x += eps
            else:
                y += eps

            # Nous verifions si la salle existe deja dans la liste selon sa position
            clone = False
            for i in range(0, len(pts)):
                if pts[i][0] == x and pts[i][1] == y:
                    clone = True
                    break

            # Position de la porte
            door_position = 0 if y > oly else 1 if x > olx else 2 if y < oly else 3
            # Ajout des portes dans la salle precedente et la suivante
            for p in pts:  # On recherche la salle precedente
                if (olx, oly) == (p[0], p[1]):
                    p[2][door_position] = 1  # Ancienne Salle
                    break
            if not clone:  # Creation de la salle si elle n'existait pas
                pts += [[x, y, [0, 0, 0, 0]]]
            for p in pts:  # On recherche la salle suivante
                if (x, y) == (p[0], p[1]):
                    p[2][(door_position + 2) % 4] = 1  # Nouvelle Salle
                    break

        idx: int
        for val in pts:
            self.rooms += [Room(val[0], val[1], val[2])]
        self.rooms[0].discover()
        self.rooms[len(self.rooms)-1].set_exit() # La derniere salle est une sortie

    def _porte(self, centrex: int, centery: int, dir: int):
        # top, right, bottom, left
        offx, offy = [[-.1, .4],
                      [.4, -.1],
                      [-.1, -.6],
                      [-.6, -.1]][dir]
        c = 'b'
        plt.gca().add_patch(
            Rectangle((centrex + offx, centery + offy),
                      0.2, 0.2, fill=True,
                      color=c, linewidth=3)
        )

    def disp_map(self, filename: str = None):
        """
        @brief affichage de la map et sauvegarde éventuelle
        @param : str fichier de sauvegarde de l'image
        """
        # stp = np.array([x.get_pos() for x in self.rooms])
        # plt.scatter(stp[:, 0], stp[:, 1])

        # clear
        plt.cla()
        plt.clf()

        # Desctivation des axes
        plt.axes(aspect='equal')
        plt.axis('off')

        # affichage des salles
        for r in self.rooms:
            if r.is_discovered():
                rom = r.get_pos()
                plt.plot([rom[0] - 0.5, rom[0] - 0.5, rom[0] + 0.5, rom[0] + 0.5, rom[0] - 0.5],
                         [rom[1] - 0.5, rom[1] + 0.5, rom[1] + 0.5, rom[1] - 0.5, rom[1] - 0.5],
                         color="black", lw=4)
                # affichage des portes
                if r.doors[r.top] == 1:
                    self._porte(rom[0], rom[1], r.top)
                if r.doors[r.left] == 1:
                    self._porte(rom[0], rom[1], r.left)
                if r.doors[r.right] == 1:
                    self._porte(rom[0], rom[1], r.right)
                if r.doors[r.bottom] == 1:
                    self._porte(rom[0], rom[1], r.bottom)

        # plt.plot(stp[:, 0], stp[:, 1])

        # affichage des liens entres les salles
        # plt.scatter(stp[0, 0], stp[0, 1], color='r', lw=4)  # entrée
        # plt.scatter(stp[-1, 0], stp[-1, 1], color='y', lw=4)  # sortie

        # sauvegarde du graph
        if filename is not None:
            # plt.savefig(filename, transparent=True)
            plt.savefig(filename, transparent=False)
        else:
            # affichage du graph
            plt.show()
