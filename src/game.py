import pygame
from pygame.locals import *
from src.view import View
from src.character import Character
from src.map import MapDungeon


class Game:
    view = None
    map = None
    character = None

    def __init__(self) -> None:
        # Initialisation de la bibliotheque Pygame
        pygame.init()

        self.view = View()

    def start_game(self):
        clock = pygame.time.Clock()

        self.map = MapDungeon(15)
        self.character = Character("Bob")

        # Boucle infinie
        close = False
        while not close:
            # Treating Events
            for event in pygame.event.get():
                if event.type == QUIT:
                    close = True
                elif event.type == VIDEORESIZE:
                    self.view.resize_event(event)

            # Calculating New sprites and Printing

            px, py = self.character.get_pos()
            self.view.print_room(self.map.get_room(px, py), self.character)
            pygame.display.flip()

            # Ticking
            clock.tick(30)
