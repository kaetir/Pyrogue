import pygame
from pygame.constants import QUIT, VIDEORESIZE, KEYDOWN, K_UP, K_DOWN, K_RIGHT, K_LEFT, K_RETURN, K_ESCAPE


from src.view import View
from src.perso.character import Character
from src.map import MapDungeon
from src.battle import Battle
from src.item import *

from src.item import Weapon


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
        self.actual_battle = None

    def dungeon_restart(self, reset):
        """
        @summary Regenere un dongeon en remettant toutes nos variables necessaire a 0
        @param reset: (si True on remet le personnage a nu et le donjon a 1)
        """
        if reset:
            self.character = Character("Bob")
            self.actual_level = 0

        self.map = MapDungeon(15)
        self.actual_level += 1
        self.character.set_pos(0, 0)
        self.map_surf = self.map.disp_map(player=self.character)
        # === TEST ===
        self.character.inventory.weapon = Weapon()
        self.character.inventory.weapon.icon_id = 11
        self.character.inventory.weapon.damage = 6
        # === FIN  ===

    def change_room(self):
        """
        @summary On avance d'une salle selon la salle ou l'on est et l'orientation du personnage
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
        self.map_surf = self.map.disp_map(player=self.character)

    def start_game(self):
        """
        @summary Algorithme principal du jeu, Main Loop algorithmique et visuelle
        """
        clock = pygame.time.Clock()

        self.dungeon_restart(True)

        # Constantes Semi-Globales de l'instance de jeu
        hud_cursor = 0
        inventory_cursor = [0, 0]
        active_cursor = [0, 0]
        max_inventory_cursor = [8 - 1, 6 - 1]
        game_area = 0  # 0: En salle, 1: En inventaire, 2: En Combat, 3: Action Objet Inventaire

        # Boucle infinie
        close = False
        while not close:
            if not self.character.is_alive():  # Reset Global
                self.dungeon_restart(True)

                # Constantes Semi-Globales de l'instance de jeu
                hud_cursor = 0
                inventory_cursor = [0, 0]
                active_cursor = [0, 0]
                game_area = 0  # 0: En salle, 1: En inventaire, 2: En Combat

            px, py = self.character.get_pos()
            current_room = self.map.get_room(px, py)
            if game_area != 6 or current_room.merchant is None:  # Si nous ne sommes pas en mode Acheter
                current_item = self.character.inventory.items[inventory_cursor[0] + inventory_cursor[1] * 8]
            else:
                current_item = current_room.merchant.inventory.items[inventory_cursor[0] + inventory_cursor[1] * 8]

            if game_area == 0 and current_room.is_exit():
                max_hud_cursor = 3
            elif game_area == 0 and current_room.merchant is not None:
                max_hud_cursor = 4
            elif game_area == 3 and isinstance(current_item, Equipment):
                max_hud_cursor = 1
            elif game_area == 3 and isinstance(current_item, Consumables):
                max_hud_cursor = 2
            else:
                max_hud_cursor = 2

            if current_room.enemy is not None and game_area != 2:
                self.actual_battle = Battle(self.character, current_room.enemy)
                game_area = 2
                print("AU COMBAT")

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
                            elif hud_cursor == 3 and current_room.merchant is not None:
                                # LES SOLDES
                                game_area = 6
                                inventory_cursor = [0, 0]
                            elif hud_cursor == 4 and current_room.merchant is not None:
                                # LES SOLDES #2
                                game_area = 7
                                inventory_cursor = [0, 0]

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

                    elif game_area == 1 or game_area == 6 or game_area == 7:  # Si on est en mode Inventaire, ou Achat ou Vente
                        if event.key == K_RETURN:
                            # Action avec l'objet du curseur, on passe en action inventaire
                            if game_area == 1 and current_item is not None:  # Si pas d'objet, on reste en mode inventaire
                                game_area = 3
                                hud_cursor = 0
                            # On achete l'objet vise
                            if game_area == 6 and current_item is not None and current_room.merchant is not None:
                                self.character.buy(current_item, current_room.merchant)
                            # On vend l'objet vise
                            if game_area == 7 and current_item is not None and current_room.merchant is not None:
                                self.character.sell(current_item, current_room.merchant)

                        elif event.key == K_ESCAPE:
                            # On quitte l'inventaire
                            inventory_cursor = [0, 0]
                            if game_area == 6:
                                hud_cursor = 3
                            elif game_area == 7:
                                hud_cursor = 4
                            else:
                                hud_cursor = 1
                            game_area = 0

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

                    elif game_area == 2:  # Si on est en mode COMBAT
                        if event.key == K_RETURN:
                            if active_cursor == [0, 0]:  # Attaque Basique
                                self.actual_battle.tour(0)
                            elif active_cursor[0] > 0 and active_cursor[1] == 0:  # Sorts
                                if self.character.inventory.active_spells[active_cursor[0] - 1] is not None:
                                    self.actual_battle.tour(active_cursor[0])
                            elif active_cursor[0] >= 0 and active_cursor[1] == 1:  # Consommables
                                if self.character.inventory.active_spells[active_cursor[0]] is not None:
                                    self.actual_battle.tour(4 + active_cursor[0])

                        elif event.key == K_UP:  # Fleche du haut
                            if active_cursor[1] > 0:
                                active_cursor[1] -= 1
                        elif event.key == K_DOWN:  # Fleche du bas
                            if active_cursor[1] < 1:
                                active_cursor[1] += 1
                        elif event.key == K_RIGHT:  # Fleche de droite
                            if active_cursor[0] < 3:
                                active_cursor[0] += 1
                        elif event.key == K_LEFT:  # Fleche de gauche
                            if active_cursor[0] > 0:
                                active_cursor[0] -= 1

                    elif game_area == 3:  # Mode Objet d'inventaire
                        if event.key == K_RETURN:
                            if isinstance(current_item, Equipment):
                                if hud_cursor == 0:
                                    self.character.inventory.equip(current_item)
                                elif hud_cursor == 1:
                                    self.character.inventory.throw(current_item)
                                game_area = 1
                            elif isinstance(current_item, SpellBook):
                                if hud_cursor == 0:
                                    active_cursor = [1, 0]
                                    game_area = 4
                                elif hud_cursor == 1:
                                    self.character.inventory.throw(current_item)
                                    game_area = 1
                            elif isinstance(current_item, Consumables):
                                if hud_cursor == 0:
                                    active_cursor = [0, 1]
                                    game_area = 5
                                elif hud_cursor == 1:
                                    self.character.inventory.throw(current_item)
                                    game_area = 1
                                elif hud_cursor == 2:
                                    self.character.inventory.use(current_item)
                                    game_area = 1

                        elif event.key == K_ESCAPE:
                            # On quitte l'interface gerant les objets d'inventaire
                            game_area = 1

                        elif event.key == K_UP:  # Fleche du haut
                            if hud_cursor > 0:
                                hud_cursor -= 1
                        elif event.key == K_DOWN:  # Fleche du bas
                            if hud_cursor < max_hud_cursor:
                                hud_cursor += 1

                    elif game_area == 4:  # Mode Objet d'inventaire -> Sorts Barre Active
                        if event.key == K_RETURN:
                            self.character.equip_spellbook(current_item, active_cursor[0] - 1)
                            active_cursor = [0, 0]
                            game_area = 1  # On retourne a l'inventaire

                        elif event.key == K_ESCAPE:
                            # On quitte l'interface gerant la barre active
                            game_area = 3

                        elif event.key == K_RIGHT:  # Fleche de droite
                            if active_cursor[0] < 3:
                                active_cursor[0] += 1
                        elif event.key == K_LEFT:  # Fleche de gauche
                            if active_cursor[0] > 1:
                                active_cursor[0] -= 1

                    elif game_area == 5:  # Mode Objet d'inventaire -> Consommables Barre Active
                        if event.key == K_RETURN:
                            self.character.equip_consumable(current_item, active_cursor[0])
                            active_cursor = [0, 0]
                            game_area = 1  # On retourne a l'inventaire

                        elif event.key == K_ESCAPE:
                            # On quitte l'interface gerant la barre active
                            game_area = 3

                        elif event.key == K_RIGHT:  # Fleche de droite
                            if active_cursor[0] < 3:
                                active_cursor[0] += 1
                        elif event.key == K_LEFT:  # Fleche de gauche
                            if active_cursor[0] > 0:
                                active_cursor[0] -= 1


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
                # HUD Right Cases
                if current_room.is_exit():
                    self.view.print_cases_hud(hud_cursor, 1)
                elif current_room.merchant is not None:
                    self.view.print_cases_hud(hud_cursor, 2)
                    # Merchant
                    self.view.print_character(current_room.merchant)
                else:
                    self.view.print_cases_hud(hud_cursor, 0)
                # HUD Active Tab
                self.view.print_active_tab(self.character)
                # HUD Fillers
                self.view.print_fillers(self.character)

            elif game_area == 1 or game_area == 6 or game_area == 7:
                # Inventory
                if game_area == 1 or game_area == 7:
                    self.view.print_inventory(self.character, inventory_cursor)
                elif game_area == 6:
                    self.view.print_inventory(current_room.merchant, inventory_cursor)
                # HUD Right Cases
                if isinstance(current_item, Equipment) or isinstance(current_item, SpellBook):
                    self.view.print_cases_hud(-1, 3)  # Si Equipement ou Sort
                elif isinstance(current_item, Consumables):
                    self.view.print_cases_hud(-1, 4)  # Si Consommable
                # HUD Active Tab
                self.view.print_active_tab(self.character)
                # Description
                # TODO
                # HUD Fillers
                self.view.print_fillers(self.character)

            elif game_area == 2:
                # Room
                self.view.print_room(current_room, self.character)
                # Monster
                self.view.print_character(current_room.enemy)
                # HUD Active Tab
                self.view.print_active_tab(self.character, active_cursor)
                # Description
                # TODO
                # HUD Fillers
                self.view.print_fillers(self.character, True)
                self.view.print_fillers(current_room.enemy, True, True) # Monstre
                # Test Fin Combat
                if self.actual_battle.is_ended():
                    game_area = 0
                    current_room.enemy = None
                    self.actual_battle = None

            elif game_area == 3:
                # Objet Inventaire
                self.view.print_inventory(self.character, inventory_cursor)
                # HUD Right Cases
                if isinstance(current_item, Equipment) or isinstance(current_item, SpellBook):
                    self.view.print_cases_hud(hud_cursor, 3)  # Si Equipement ou Sort
                elif isinstance(current_item, Consumables):
                    self.view.print_cases_hud(hud_cursor, 4)  # Si Consommable
                # HUD Active Tab
                self.view.print_active_tab(self.character)
                # Description
                # TODO
                # HUD Fillers
                self.view.print_fillers(self.character)

            elif game_area == 4 or game_area == 5:
                # Objet d'inventaire -> Sorts Barre Active
                self.view.print_inventory(self.character, inventory_cursor)
                # HUD Right Cases
                if isinstance(current_item, Equipment) or isinstance(current_item, SpellBook):
                    self.view.print_cases_hud(-1, 3)  # Si Equipement ou Sort
                elif isinstance(current_item, Consumables):
                    self.view.print_cases_hud(-1, 4)  # Si Consommable
                # HUD Active Tab
                self.view.print_active_tab(self.character, active_cursor)
                # Description
                # TODO
                # HUD Fillers
                self.view.print_fillers(self.character)

            # HUD Active Equipment
            self.view.print_active_equipment(self.character)

            pygame.display.flip()

            # Ticking
            clock.tick(30)
