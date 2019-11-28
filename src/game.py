import pygame
from pygame.constants import QUIT, VIDEORESIZE, KEYDOWN, K_UP, K_DOWN, K_RIGHT, K_LEFT, K_RETURN, K_ESCAPE

from src.view import View
from src.perso.character import Character
from src.map import MapDungeon
from src.battle import Battle
from src.item import *

from src.item import Weapon
from src.db.db import PyrogueDB
from src.stats_and_achievement import Achiever


class Game:
    view = None
    map = None
    character = None
    actual_level = 0
    db = PyrogueDB()

    def __init__(self) -> None:

        self.view = View()
        self.map_surf: str = ""
        self.actual_battle = None
        pygame.display.set_caption("Pyrogue : la commutativité de l’anneau")

    def dungeon_restart(self, reset):
        """
        @summary Regenere un dongeon en remettant toutes nos variables necessaire a 0
        @param reset: (si True on remet le personnage a nu et le donjon a 1)
        """
        if reset:
            self.character = Character("Bob")
            self.actual_level = 0
            # === TEST ===
            self.character.inventory.weapon = Weapon("weapon")
            self.character.inventory.append(Armor())
            self.character.inventory.append(Weapon())
            self.character.inventory.append(SpellBook())
            # === FIN  ===time.sleep(2

        self.map = MapDungeon(15)
        self.actual_level += 1
        self.character.set_pos(0, 0)
        self.map_surf = self.map.disp_map(player=self.character)
        self.character.inventory.append(Consumables())

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
            Achiever.stats["Room découvertes"] += 1
            Achiever.achievements["100 Rooms discovered"] = Achiever.stats["Room découvertes"] >= 100
            self.map.get_room(px, py).discover()
            self.character.gain_xp(1)
            self.character.mana += 1 if self.character.mana < self.character.max_mana else 0
        self.map_surf = self.map.disp_map(player=self.character)

    def start_game(self):
        """
        @summary Algorithme principal du jeu, Main Loop algorithmique et visuelle
        """
        clock = pygame.time.Clock()

        self.dungeon_restart(True)

        # Constantes Semi-Globales de l'instance de jeu
        menu_cursor = 0
        max_inventory_cursor = [8 - 1, 6 - 1]
        current_game = False
        # game_area =  0: En salle, 1: En inventaire, 2: En Combat, 3: Action Objet Inventaire
        reac_j, reac_m = 0, 0  # les reaction des joueur ou mob apres une attaque  cf : tour

        # Boucle infinie
        in_game = False
        in_menu = True
        close = False
        bdd_error = False

        while not close:
            # boucle Infinie du menu
            parallax_position = 0
            """
            #     #  #######  #     #  #     # 
            ##   ##  #        ##    #  #     # 
            # # # #  #        # #   #  #     # 
            #  #  #  #####    #  #  #  #     # 
            #     #  #        #   # #  #     # 
            #     #  #        #    ##  #     # 
            #     #  #######  #     #   #####  
            """
            while in_menu:
                for event in pygame.event.get():
                    if event.type == QUIT:  # On quitte le jeu
                        in_menu = False
                        in_game = False
                        close = True
                    elif event.type == VIDEORESIZE:
                        self.view.resize_event(event)

                    elif event.type == KEYDOWN:  # On gere les boutons
                        if event.key == K_ESCAPE:  # On quitte le jeu
                            in_menu = False
                            in_game = False
                            close = True

                        elif event.key == K_RETURN:
                            Achiever.stats, Achiever.achievements = self.db.load_stats_and_achievement()
                            if menu_cursor == 0 and not current_game:
                                # Nouvelle Partie
                                self.dungeon_restart(True)
                                in_game = True
                                in_menu = False

                            elif menu_cursor == 0 and current_game:
                                # Continue la partie
                                in_game = True
                                in_menu = False

                            elif menu_cursor == 1 and not current_game:
                                # Charge une partie
                                tmp = self.db.load()
                                if not isinstance(tmp, int):
                                    self.character, self.map, self.actual_level = self.db.load()
                                    self.map_surf = self.map.disp_map(player=self.character)
                                    in_game = True
                                    in_menu = False
                                else:
                                    print("Erreur de connection a la BDD")
                                    bdd_error = True

                            elif menu_cursor == 1 and not current_game:
                                # Sauvegarde la partie en cours
                                self.db.save(self)

                        elif event.key == K_UP:  # Fleche du haut
                            if menu_cursor > 0:
                                menu_cursor -= 1
                                bdd_error = False
                        elif event.key == K_DOWN:  # Fleche du bas
                            if menu_cursor < 3:
                                menu_cursor += 1
                                bdd_error = False
                """                
                ####            #            #       #
                #   #                        #
                #   #  # ##    ##    # ##   ####    ##    # ##    ## #
                ####   ##  #    #    ##  #   #       #    ##  #  #  #
                #      #        #    #   #   #       #    #   #   ##
                #      #        #    #   #   #  #    #    #   #  #
                #      #       ###   #   #    ##    ###   #   #   ###
                                                                #   #
                                                                ###
                """
                # Background
                parallax_position += 1
                self.view.print_parallax_background(parallax_position)

                # Cases
                self.view.print_cases_menu(menu_cursor, current_game)

                # BDD error
                if bdd_error:
                    self.view.print_info_on_menu({"Erreur bdd": str(tmp)}, "ALED LA BDD A EXPLOSE")

                # Succes
                if menu_cursor == 2:
                    self.view.print_info_on_menu(Achiever.achievements, "Succes")

                # Stats
                elif menu_cursor == 3:
                    self.view.print_info_on_menu(Achiever.stats, "Stats")

                pygame.display.flip()

                # Ticking
                clock.tick(30)

            # Boucle Infinie du jeu
            game_area = 0
            hud_cursor = 0
            inventory_cursor = [0, 0]
            active_cursor = [0, 0]
            reac_fading = 0
            """
            ###    #     #        #####        #       #     #    ####### 
             #     ##    #       #     #      # #      ##   ##    #         
             #     # #   #       #           #   #     # # # #    #       
             #     #  #  #       #  ####    #     #    #  #  #    #####   
             #     #   # #       #     #    #######    #     #    #       
             #     #    ##       #     #    #     #    #     #    #       
            ###    #     #        #####     #     #    #     #    ####### 
                                                                            
            """
            while in_game:
                current_game = True
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
                """
                ###                      #     #                      ####                     #
                 #                       #                            #                        #
                 #    ###    ##    ###  ###   ##    ###    ###        ###   # #    ##   ###   ###    ###
                 #    #  #  # ##  #  #   #     #    #  #  #  #        #     # #   # ##  #  #   #    ##
                 #    #     ##    # ##   #     #    #  #   ##         #     # #   ##    #  #   #      ##
                 #    #      ##    # #    ##  ###   #  #  #           ####   #     ##   #  #    ##  ###
                                                           ###
                """
                for event in pygame.event.get():
                    if event.type == QUIT:
                        in_menu = False
                        in_game = False
                        close = True
                    elif event.type == VIDEORESIZE:
                        self.view.resize_event(event)

                    elif event.type == KEYDOWN:  # On gere les boutons
                        if game_area == 0:  # Si on est en mode salles
                            if event.key == K_ESCAPE:  # Retour a l'ecran d'accueil
                                in_game = False
                                in_menu = True
                                # TODO Save ?
                                self.db.save_stats_and_achievement(Achiever.stats, Achiever.achievements)
                            elif event.key == K_RETURN:
                                if hud_cursor == 1:
                                    # INVENTAIRE
                                    game_area = 1
                                    inventory_cursor = [0, 0]
                                elif hud_cursor == 2:
                                    self.db.save(self)
                                    print("Saving ...")  # SAVE
                                elif hud_cursor == 3 and current_room.is_exit():
                                    # CHANGEMENT DE DONJON
                                    hud_cursor = 0
                                    self.dungeon_restart(False)  # Sans RESET
                                elif hud_cursor == 3 and current_room.merchant is not None:
                                    # Mode achat
                                    game_area = 6
                                    inventory_cursor = [0, 0]
                                elif hud_cursor == 4 and current_room.merchant is not None:
                                    # Mode vente
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
                                Achiever.stats["Rotations"] += 1
                            elif event.key == K_LEFT and hud_cursor == 0:
                                self.character.set_orientation((self.character.get_orientation() - 1) % 4)
                                self.map_surf = self.map.disp_map(player=self.character)
                                Achiever.stats["Rotations"] += 1

                        # Si on est en mode Inventaire, ou Achat ou Vente
                        elif game_area == 1 or game_area == 6 or game_area == 7:
                            if event.key == K_RETURN:
                                # Action avec l'objet du curseur, on passe en action inventaire
                                # Si objet -> menu contextuel de celui-ci
                                if game_area == 1 and current_item is not None:
                                    game_area = 3
                                    hud_cursor = 0
                                # Si pas d'objet, on echange avec un consommable
                                elif game_area == 1 and current_item is None:
                                    active_cursor = [0, 1]
                                    game_area = 5
                                # On achete l'objet vise
                                elif game_area == 6 and current_item is not None and current_room.merchant is not None:
                                    self.character.buy(current_item, current_room.merchant)
                                # On vend l'objet vise
                                elif game_area == 7 and current_item is not None and current_room.merchant is not None:
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
                                    reac_j, reac_m = self.actual_battle.tour(0)
                                    reac_fading = 1 if reac_j != 0 and reac_m != 0 else 0
                                elif active_cursor[0] > 0 and active_cursor[1] == 0:  # Sorts
                                    if self.character.inventory.active_spells[active_cursor[0] - 1] is not None:
                                        reac_j, reac_m = self.actual_battle.tour(active_cursor[0])
                                        reac_fading = 1 if reac_j != 0 and reac_m != 0 else 0
                                elif active_cursor[0] >= 0 and active_cursor[1] == 1:  # Consommables
                                    if self.character.inventory.active_comsumable[active_cursor[0]] is not None:
                                        reac_j, reac_m = self.actual_battle.tour(4 + active_cursor[0])
                                        reac_fading = 1 if reac_j != 0 and reac_m != 0 else 0

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
                            if event.key == K_RETURN:  # Selection d'un objet
                                if isinstance(current_item, Equipment):  # Equipement
                                    if hud_cursor == 0:
                                        self.character.equip(current_item)
                                    elif hud_cursor == 1:
                                        self.character.inventory.throw(current_item)
                                    game_area = 1
                                elif isinstance(current_item, SpellBook):  # Sort
                                    if hud_cursor == 0:
                                        active_cursor = [1 if None not in self.character.inventory.active_spells else
                                                         self.character.inventory.active_spells.index(None) + 1, 0]
                                        game_area = 4
                                    elif hud_cursor == 1:
                                        self.character.inventory.throw(current_item)
                                        game_area = 1
                                elif isinstance(current_item, Consumables):  # Consommable
                                    if hud_cursor == 0:
                                        active_cursor = [
                                            0 if None not in self.character.inventory.active_comsumable else
                                            self.character.inventory.active_comsumable.index(None), 1]
                                        game_area = 5
                                    elif hud_cursor == 1:
                                        self.character.inventory.throw(current_item)
                                        game_area = 1
                                    elif hud_cursor == 2:
                                        if isinstance(current_item, Consumables):
                                            if current_item.bonus:
                                                self.character.inventory.use(current_item, self.character)
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
                                self.character.inventory.equip_spellbook(current_item, active_cursor[0] - 1)
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
                                if current_item is None:
                                    # Si on, est arrive ici depuis l'inventaire pour desequiper un consommable
                                    game_area = 1
                                else:  # Sinon qu'on cherchait a en equiper un
                                    game_area = 3

                            elif event.key == K_RIGHT:  # Fleche de droite
                                if active_cursor[0] < 3:
                                    active_cursor[0] += 1
                            elif event.key == K_LEFT:  # Fleche de gauche
                                if active_cursor[0] > 0:
                                    active_cursor[0] -= 1

                """                
                ####            #            #       #
                #   #                        #
                #   #  # ##    ##    # ##   ####    ##    # ##    ## #
                ####   ##  #    #    ##  #   #       #    ##  #  #  #
                #      #        #    #   #   #       #    #   #   ##
                #      #        #    #   #   #  #    #    #   #  #
                #      #       ###   #   #    ##    ###   #   #   ###
                                                                #   #
                                                                ###
                """
                # Calculating New sprites and Printing
                px, py = self.character.get_pos()
                current_room = self.map.get_room(px, py)
                # Background
                self.view.print_clear()

                # HUD Active Equipment
                self.view.print_active_equipment(self.character)

                if game_area == 0:
                    # Room
                    self.view.print_room(current_room, self.character)
                    # Map
                    self.view.print_map(self.map_surf)
                    # Game Infos
                    self.view.print_game_infos(self.character, self.actual_level)
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
                    if game_area == 1:
                        if isinstance(current_item, Equipment) or isinstance(current_item, SpellBook):
                            self.view.print_cases_hud(-1, 3)  # Si Equipement ou Sort
                        elif isinstance(current_item, Consumables):
                            self.view.print_cases_hud(-1, 4)  # Si Consommable
                    # HUD Active Tab
                    self.view.print_active_tab(self.character)
                    # Description
                    self.view.print_description(current_item)
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
                    self.view.print_fillers(current_room.enemy, True, True)  # Monstre
                    # HUD Icons Reac
                    if reac_fading > 0:
                        self.view.print_reaction_icon(reac_m, reac_fading)
                        self.view.print_reaction_icon(reac_j, reac_fading, True)
                        reac_fading -= 0.05
                    # Test Fin Combat
                    if self.actual_battle.is_ended():
                        game_area = 0
                        current_room.enemy = None
                        self.actual_battle = None
                        reac_fading = 0

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
                    self.view.print_description(current_item)
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
                    self.view.print_description(current_item)
                    # HUD Fillers
                    self.view.print_fillers(self.character)

                pygame.display.flip()

                if not self.character.is_alive():  # On quitte la partie #DEAD
                    current_game = False
                    in_game = False
                    in_menu = True

                # Ticking
                clock.tick(30)
