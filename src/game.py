import pygame
from pygame.locals import *
from src.view import View
from src.character import Character
from src.map import MapDungeon
from src.item import Item

from math import floor
from random import random

class Game:
    view = None
    map = None
    character = None
    actual_level = 0

    def __init__(self) -> None:
        # Initialisation de la bibliotheque Pygame
        pygame.init()

        self.view = View()

    def dungeon_restart(self, reset):
        """
        @brief Regenere un dongeon en remettant toutes nos variables necessaire a 0
        :param reset: (si True on remet le personnage a nu et le donjon a 1)
        """
        if reset:
            self.character = Character("Bob")
            self.actual_level = 0

        self.map = MapDungeon(15)
        self.map.disp_map("map.png")
        self.actual_level += 1
        self.character.set_pos(0, 0)


    def change_room(self):
        """
        @brief On avance d'une salle selon la salle ou l'on est et l'orientation du personnage
        """
        px, py = self.character.get_pos()
        room = self.map.get_room(px, py)
        orient = self.character.get_orientation()
        if room.get_doors()[orient] == 0:
            return False  # On ne peut pas avancer, c'est un mur!
        # else Calcul de la nouvel position selon l'orientation
        if orient == 0:
            py += 1
        elif orient == 1:
            px += 1
        elif orient == 2:
            py -= 1
        elif orient == 3:
            px -= 1

        self.character.set_pos(px, py)
        self.map.get_room(px, py).discover()
        self.map.disp_map("map.png")

    def start_game(self):
        """
        @brief Algorithme principal du jeu, Main Loop algorithmique et visuelle
        """
        clock = pygame.time.Clock()

        self.dungeon_restart(True)

        # TESTS ------
        self.character.health = 12
        self.character.mana = 3
        for i in range(0, floor(8*5 * random())):
            it = Item()
            it.set_icon_id(floor(random() * 70))
            self.character.collect(it)
        # FIN TESTS ---

        # Constantes Semi-Globales de l'instance de jeu
        hud_cursor = 0
        max_hud_cursor = 2
        inventory_cursor = [0, 0]
        max_inventory_cursor = [8-1, 6-1]
        game_area = 0  # 0: En salle, 1: En inventaire

        # Boucle infinie
        close = False
        while not close:
            px, py = self.character.get_pos()
            current_room = self.map.get_room(px, py)

            if current_room.is_exit():
                max_hud_cursor = 3
            else:
                max_hud_cursor = 2

            # Treating Events
            for event in pygame.event.get():
                if event.type == QUIT:
                    close = True
                elif event.type == VIDEORESIZE:
                    self.view.resize_event(event)

                elif event.type == pygame.KEYDOWN:  # On gere les boutons
                    if game_area == 0:  # Si on est en mode salles
                        if event.key == pygame.K_RETURN:
                            if hud_cursor == 1:
                                # INVENTAIRE
                                game_area = 1
                                inventory_cursor = [0, 0]
                            elif hud_cursor == 2:
                                i=1# SAVE
                            elif hud_cursor == 3 and current_room.is_exit():
                                # CHANGEMENT DE DONJON
                                hud_cursor = 0
                                self.dungeon_restart(False)  # Sans RESET

                        elif event.key == pygame.K_UP:  # Fleche du haut
                            if hud_cursor > 0:
                                hud_cursor -= 1
                            elif hud_cursor == 0:  # Si nous sommes sur la case de mouvement, on change de salle (si possible)
                                self.change_room()
                        elif event.key == pygame.K_DOWN:  # Fleche du bas
                            if hud_cursor < max_hud_cursor:
                                hud_cursor += 1

                        # Si nous sommes sur la case_HUD (0) de mouvement et que nous effectuons une rotation
                        elif event.key == pygame.K_RIGHT and hud_cursor == 0:
                            self.character.set_orientation((self.character.get_orientation() + 1) % 4)
                        elif event.key == pygame.K_LEFT and hud_cursor == 0:
                            self.character.set_orientation((self.character.get_orientation() - 1) % 4)

                    elif game_area == 1:  # Si on est en mode Inventaire
                        if event.key == pygame.K_RETURN:
                            # Action avec l'objet du curseur
                            i=1

                        elif event.key == pygame.K_ESCAPE:
                            # On quitte l'inventaire
                            game_area = 0

                        elif event.key == pygame.K_UP:  # Fleche du haut
                            if inventory_cursor[1] > 0:
                                inventory_cursor[1] -= 1
                        elif event.key == pygame.K_DOWN:  # Fleche du bas
                            if inventory_cursor[1] < max_inventory_cursor[1]:
                                inventory_cursor[1] += 1
                        elif event.key == pygame.K_RIGHT:  # Fleche de droite
                            if inventory_cursor[0] < max_inventory_cursor[0]:
                                inventory_cursor[0] += 1
                        elif event.key == pygame.K_LEFT:  # Fleche de gauche
                            if inventory_cursor[0] > 0:
                                inventory_cursor[0] -= 1

            # Calculating New sprites and Printing
            px, py = self.character.get_pos()
            current_room = self.map.get_room(px, py)
            # Background
            self.view.print_clear()

            if game_area == 0:
                # Room
                self.view.print_room(current_room, self.character)
            elif game_area == 1:
                # Room
                self.view.print_inventory(self.character, inventory_cursor)

            # Map
            self.view.print_map()
            # HUD Right Cases
            self.view.print_cases_hud(hud_cursor, current_room.is_exit())
            # HUD Active Tab
            self.view.print_active_tab(self.character)
            # HUD Fillers
            self.view.print_fillers(self.character)

            pygame.display.flip()

            # Ticking
            clock.tick(30)
