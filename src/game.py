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
        """
        @brief Algorithme principal du jeu, Main Loop algorithmique et visuelle
        """
        clock = pygame.time.Clock()

        self.map = MapDungeon(15)
        self.character = Character("Bob")

        hud_cursor = 0

        # Boucle infinie
        close = False
        while not close:
            # Treating Events
            for event in pygame.event.get():
                if event.type == QUIT:
                    close = True
                elif event.type == VIDEORESIZE:
                    self.view.resize_event(event)

                elif event.type == pygame.KEYDOWN: # On gere les boutons
                    if event.key == pygame.K_UP: # Fleche du haut
                        if hud_cursor > 0:
                            hud_cursor -= 1
                    elif event.key == pygame.K_DOWN: # Fleche du bas
                        if hud_cursor < 3:
                            hud_cursor += 1
                    # Si nous sommes sur la case de mouvement et que nous effectuons une rotation
                    elif event.key == pygame.K_RIGHT and hud_cursor == 0:
                        self.character.set_orientation((self.character.get_orientation() + 1) % 4)
                    elif event.key == pygame.K_LEFT and hud_cursor == 0:
                        self.character.set_orientation((self.character.get_orientation() - 1) % 4)
            # Calculating New sprites and Printing
            # Background
            self.view.print_clear()
            # Room
            px, py = self.character.get_pos()
            self.view.print_room(self.map.get_room(px, py), self.character)
            # Map
            self.map.disp_map("map.png")
            self.view.print_map()
            #HUD Right Cases
            self.view.print_cases_hud(hud_cursor)

            pygame.display.flip()

            # Ticking
            clock.tick(30)
