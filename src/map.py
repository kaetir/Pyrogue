"""
- Map has Rooms and are bound each other linearly,

"""

from math import floor
from random import random

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from matplotlib.patches import Rectangle
import matplotlib.backends.backend_agg as agg

from src.room import Room
from src.character import Character


class MapDungeon:
    fig = plt.figure()

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
        self.rooms[len(self.rooms) - 1].set_exit()  # La derniere salle est une sortie

    def _porte(self, plot, centerx: int, centery: int, dir: int):
        # top, right, bottom, left
        offx, offy = [[-.1, .4],
                      [.4, -.1],
                      [-.1, -.6],
                      [-.6, -.1]][dir]
        c = 'w'
        l = 0.2
        x = [centerx + offx, centerx + offx + l, centerx + offx + l, centerx + offx, centerx + offx ]
        y = [centery + offy, centery + offy    , centery + offy + l, centery + offy + l, centery + offy]
        plot.fill(x, y, c, zorder=3)
        return plot

    def disp_map(self, filename: str = None, player: Character = None):
        """
        @brief affichage de la map et sauvegarde éventuelle
        @param : str fichier de sauvegarde de l'image
        @param : Character le personnage principale
        """

        # Desctivation des axes
        ax = self.fig.add_subplot(111, aspect="equal")
        ax.axis("off")

        # affichage des salles
        for r in self.rooms:
            if r.is_discovered():
                rom = r.get_pos()
                ax.plot([rom[0] - 0.5, rom[0] - 0.5, rom[0] + 0.5, rom[0] + 0.5, rom[0] - 0.5],
                        [rom[1] - 0.5, rom[1] + 0.5, rom[1] + 0.5, rom[1] - 0.5, rom[1] - 0.5],
                        color="r", lw=4)

            # affichage des portes
                if r.doors[r.top] == 1:
                    self._porte(ax, rom[0], rom[1], r.top)
                if r.doors[r.left] == 1:
                    self._porte(ax, rom[0], rom[1], r.left)
                if r.doors[r.right] == 1:
                    self._porte(ax, rom[0], rom[1], r.right)
                if r.doors[r.bottom] == 1:
                    self._porte(ax, rom[0], rom[1], r.bottom)

        if player is not None:
            m = ["^", ">", "v", "<"][player.get_orientation()]
            ax.scatter(player.position[0], player.position[1], s=100, c="y", marker=m)

        # sauvegarde du graph
        if filename is not None:
            self.fig.savefig(filename, transparent=True)
        else:
            # affichage du graph
            canvas = agg.FigureCanvasAgg(self.fig)
            canvas.draw()
            renderer = canvas.get_renderer()
            raw_data = renderer.tostring_rgb()
            size = canvas.get_width_height()
            self.fig.delaxes(ax)
            return raw_data, size
