"""
- Map has Rooms and are bound each other linearly,

"""

from math import floor
from random import random

import matplotlib

import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg

from src.room import Room
from src.perso.character import Character

matplotlib.use("Agg")


class MapDungeon:
    fig = plt.figure()

    def __init__(self, size: int = 15) -> None:
        """
        @summary constructeur
        @param : int taille de la carte
        """
        super().__init__()
        self.rooms = []
        self.map_size = size
        self.gen_map(size)

    def __str__(self) -> str:
        """
        @summary fonciton pour le retour string
        """
        return self.rooms.__str__()

    def get_room(self, x, y):
        """
        @summary renvoie une room en fonction de ses coordonnées
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
        @summary generateur de carte aléatoire sur le model de l'algo du marcheur
        @param : int taille de la carte
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
        self.rooms[0].enemy = None
        self.rooms[0].merchant = None
        self.rooms[len(self.rooms) - 1].set_exit()  # La derniere salle est une sortie
        self.rooms[len(self.rooms) - 1].enemy = None
        self.rooms[len(self.rooms) - 1].merchant = None

    @staticmethod
    def _porte(plot, centerx: int, centery: int, dire: int):
        # top, right, bottom, left
        offx, offy = [[-.1, .4],
                      [.4, -.1],
                      [-.1, -.6],
                      [-.6, -.1]][dire]
        c = '#595652'
        largeur_porte = 0.2
        x = [centerx + offx, centerx + offx + largeur_porte,
             centerx + offx + largeur_porte, centerx + offx, centerx + offx]
        y = [centery + offy, centery + offy, centery + offy + largeur_porte,
             centery + offy + largeur_porte, centery + offy]
        plot.fill(x, y, c, zorder=3)
        return plot

    def disp_map(self, filename: str = None, player: Character = None):
        """
        @summary affichage de la carte et sauvegarde éventuelle
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
                x = [rom[0] - .5, rom[0] + .5, rom[0] + .5, rom[0] - .5, rom[0] - .5]
                y = [rom[1] - .5, rom[1] - .5, rom[1] + .5, rom[1] + .5, rom[1] - .5]
                ax.fill(x, y, "#595652", zorder=1)
                ax.plot([rom[0] - 0.5, rom[0] - 0.5, rom[0] + 0.5, rom[0] + 0.5, rom[0] - 0.5],
                        [rom[1] - 0.5, rom[1] + 0.5, rom[1] + 0.5, rom[1] - 0.5, rom[1] - 0.5],
                        color="#d27d2c", lw=4)

                # affichage des portes
                for direction in [r.top, r.left, r.right, r.bottom]:
                    if r.doors[direction] == 1:
                        self._porte(ax, rom[0], rom[1], direction)

                if r.merchant is not None:
                    size_cursor = ax.get_ylim()[1] - ax.get_ylim()[0]
                    ax.scatter(rom[0], rom[1], s=(10 - size_cursor) * 100, c="y",
                               marker="o", zorder=3)

        if self.rooms[-1].is_discovered():
            ax.scatter(self.rooms[-1].get_pos()[0], self.rooms[-1].get_pos()[1], s=100, c="b", marker="X")

        if player is not None:
            m = ["^", ">", "v", "<"][player.get_orientation()]
            size_cursor = ax.get_ylim()[1] - ax.get_ylim()[0]
            ax.scatter(player.position[0], player.position[1], s=(10 - size_cursor) * 100, c="#5555ff",
                       marker=m, zorder=3)

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
