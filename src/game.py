import pygame
from pygame.constants import QUIT, VIDEORESIZE, KEYDOWN, K_UP, K_DOWN, K_RIGHT, K_LEFT, K_RETURN, K_ESCAPE

from src.view import View
from src.perso.character import Character
from src.map import MapDungeon
from src.battle import Battle


class Game:
    view = None
    map = None
    character = None
    actual_level = 0

    def __init__(self) -> None:
        # Initialisation de la bibliotheque Pygame
        # pygame.init()
        # cassé ne pas faire LOL

        self.view = View()
        self.map_surf: str = ""

    def dungeon_restart(self, reset):
        """
        @brief Regenere un dongeon en remettant toutes nos variables necessaire a 0
        :param reset: (si True on remet le personnage a nu et le donjon a 1)
        """
        if reset:
            self.character = Character("Bob")
            self.actual_level = 0

        self.map = MapDungeon(15)
        self.actual_level += 1
        self.character.set_pos(0, 0)
        self.map_surf = self.map.disp_map(player=self.character)

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
        if not self.map.get_room(px, py).is_discovered():
            self.map.get_room(px, py).discover()
            self.character.gain_xp(1)
            if self.map.get_room(px, py).enemy is not None:
                # TODO
                # disp sprite mob
                # begin combat
                labaston = Battle(self.character, self.map.get_room(px, py).enemy)
                print("AU COMBAT")
        self.map_surf = self.map.disp_map(player=self.character)

    def start_game(self):
        """
        @brief Algorithme principal du jeu, Main Loop algorithmique et visuelle
        """
        clock = pygame.time.Clock()

        self.dungeon_restart(True)

        # Constantes Semi-Globales de l'instance de jeu
        hud_cursor = 0
        inventory_cursor = [0, 0]
        max_inventory_cursor = [8 - 1, 6 - 1]
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

                elif event.type == KEYDOWN:  # On gere les boutons
                    if game_area == 0:  # Si on est en mode salles
                        if event.key == K_RETURN:
                            if hud_cursor == 1:
                                # INVENTAIRE
                                game_area = 1
                                inventory_cursor = [0, 0]
                            elif hud_cursor == 2:
                                # TODO
                                print("TODO Save")  # SAVE
                            elif hud_cursor == 3 and current_room.is_exit():
                                # CHANGEMENT DE DONJON
                                hud_cursor = 0
                                self.dungeon_restart(False)  # Sans RESET

                        elif event.key == K_UP:  # Fleche du haut
                            if hud_cursor > 0:
                                hud_cursor -= 1
                            # Si nous sommes sur la case de mouvement, on change de salle (si possible)
                            elif hud_cursor == 0:
                                self.change_room()
                        elif event.key == K_DOWN:  # Fleche du bas
                            if hud_cursor < max_hud_cursor:
                                hud_cursor += 1

                        # Si nous sommes sur la case_HUD (0) de mouvement et que nous effectuons une rotation
                        elif event.key == K_RIGHT and hud_cursor == 0:
                            self.character.set_orientation((self.character.get_orientation() + 1) % 4)
                            self.map_surf = self.map.disp_map(player=self.character)
                        elif event.key == K_LEFT and hud_cursor == 0:
                            self.character.set_orientation((self.character.get_orientation() - 1) % 4)
                            self.map_surf = self.map.disp_map(player=self.character)

                    elif game_area == 1:  # Si on est en mode Inventaire
                        if event.key == K_RETURN:
                            # Action avec l'objet du curseur
                            # TODO
                            print("TODO équiper")

                        elif event.key == K_ESCAPE:
                            # On quitte l'inventaire
                            game_area = 0
                            hud_cursor = 1

                        elif event.key == K_UP:  # Fleche du haut
                            if inventory_cursor[1] > 0:
                                inventory_cursor[1] -= 1
                        elif event.key == K_DOWN:  # Fleche du bas
                            if inventory_cursor[1] < max_inventory_cursor[1]:
                                inventory_cursor[1] += 1
                        elif event.key == K_RIGHT:  # Fleche de droite
                            if inventory_cursor[0] < max_inventory_cursor[0]:
                                inventory_cursor[0] += 1
                        elif event.key == K_LEFT:  # Fleche de gauche
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
                # Map
                self.view.print_map(self.map_surf)
            elif game_area == 1:
                # Inventory
                self.view.print_inventory(self.character, inventory_cursor)
                # Description

            # HUD Right Cases
            self.view.print_cases_hud(hud_cursor, current_room.is_exit())
            # HUD Active Equipment
            self.view.print_active_equipment(self.character)
            # HUD Active Tab
            self.view.print_active_tab(self.character)
            # HUD Fillers
            self.view.print_fillers(self.character)

            pygame.display.flip()

            # Ticking
            clock.tick(30)
