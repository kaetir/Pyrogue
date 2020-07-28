import pygame
from pygame.locals import RESIZABLE

from item import Item
from perso.merchant import Merchant
from perso.monster import Monster
from item import Item
from res.ressources_id import *


def load_tile_table(filename, nbx: int, nby: int, colorkey=None):
    """
    @summary Charge un spritesheet selon une image et le nombre de sprites
    @param filename : nom du fichier
    @param nbx : nombre de sprites horizontaux
    @param nby : nombre de sprites verticaux
    @param colorkey : charge une image non transparente en transformant une couleur transparente
    @return : un tableau de surfaces contenant les sprites
    """
    if colorkey is not None:
        image = pygame.image.load(filename).convert()
        image.set_colorkey(colorkey)
    else:
        image = pygame.image.load(filename).convert_alpha()
    image_width, image_height = image.get_size()
    tile_table = []

    for tile_y in range(0, nby):
        for tile_x in range(0, nbx):
            rect = (tile_x * image_width // nbx, tile_y * image_height //
                    nby, image_width // nbx, image_height // nby)
            tile_table.append(image.subsurface(rect))
    return tile_table


class View:
    window = None
    wwidth, wheight = 0, 0
    # Assets
    wall_tiles = None
    door_tiles = None
    ceiling_tiles = None
    cases_hud = None
    fills_fillers = None
    fills_tips = None
    fills_main = None
    fills_tubes = None
    numbers_tiles = None
    inventory_tab = None
    inventory_cursor = None
    active_tab = None
    active_equipment = None
    items_tiles = None
    description_tiles = None
    hud_icons = None

    # Assets Parallax
    parallax = []

    # Assets Monsters
    monsters = []
    # Assets Merchants
    merchants = []
    # Font
    font_name = None
    fonts_stock = {}

    # Stock les polices selon leurs tailles
    # #(evite de reouvrir la police chaque fois que l'on reecri a la meme taille)

    def __init__(self) -> None:
        # Creation de la fenetre
        self.window = pygame.display.set_mode((800, 450), RESIZABLE)
        self.wwidth, self.wheight = pygame.display.get_surface().get_size()

        pygame.font.init()

        self.load_assets()
        self.parallax_scaled = []

        class tmp:
            size = (800, 450)

        self.resize_event(tmp())

    def load_assets(self):
        """
        @summary Charge les sprites necessaires au bon fonctionnement du jeu
        """
        # Assets
        self.wall_tiles = load_tile_table(
            "../res/tiles/dungeon_wall.png", 4, 4)
        self.door_tiles = load_tile_table(
            "../res/tiles/dungeon_door.png", 4, 4)
        self.ceiling_tiles = load_tile_table(
            "../res/tiles/dungeon_ceiling.png", 4, 4)
        self.cases_hud = load_tile_table("../res/hud/cases.png", 1, 4)
        self.fills_fillers = load_tile_table(
            "../res/hud/fills_fillers.png", 1, 4)
        self.fills_tips = load_tile_table("../res/hud/fills_tips.png", 1, 4)
        self.fills_main = load_tile_table("../res/hud/fills_main.png", 5, 1)
        self.fills_tubes = load_tile_table("../res/hud/fills_tubes.png", 1, 1)
        self.numbers_tiles = load_tile_table("../res/hud/numbers.png", 11, 1)
        self.inventory_tab = load_tile_table(
            "../res/inventory/inventory_tab.png", 1, 1)
        self.inventory_cursor = load_tile_table(
            "../res/inventory/inventory_cursor.png", 1, 1)
        self.active_tab = load_tile_table(
            "../res/inventory/active_tab.png", 1, 1)
        self.active_equipment = load_tile_table(
            "../res/inventory/active_equipment.png", 1, 1)
        self.items_tiles = load_tile_table(
            "../res/inventory/items.png", 10, 11)
        self.description_tiles = load_tile_table(
            "../res/hud/description.png", 1, 1)
        self.hud_icons = load_tile_table(
            "../res/hud/hud_icons.png", 3, 1, (255, 0, 255))

        # Assets Parallax
        self.parallax.append(pygame.image.load(
            "../res/menu/parallax/background0.png").convert_alpha())
        self.parallax.append(pygame.image.load(
            "../res/menu/parallax/background1.png").convert_alpha())
        self.parallax.append(pygame.image.load(
            "../res/menu/parallax/background2.png").convert_alpha())
        self.parallax.append(pygame.image.load(
            "../res/menu/parallax/background3.png").convert_alpha())
        self.parallax.append(pygame.image.load(
            "../res/menu/parallax/background4.png").convert_alpha())
        self.parallax.append(pygame.image.load(
            "../res/menu/parallax/background5.png").convert_alpha())

        # Assets Monsters
        self.monsters.append(pygame.image.load(
            "../res/enemies/druid.png").convert_alpha())
        self.monsters.append(pygame.image.load(
            "../res/enemies/imp.png").convert_alpha())
        self.monsters.append(pygame.image.load(
            "../res/enemies/mimic.png").convert_alpha())
        self.monsters.append(pygame.image.load(
            "../res/enemies/skeleton.png").convert_alpha())
        self.monsters.append(pygame.image.load(
            "../res/enemies/zombie.png").convert_alpha())
        self.monsters.append(pygame.image.load(
            "../res/enemies/shadow_soul.png").convert_alpha())

        # Assets Merchants
        self.merchants.append(pygame.image.load(
            "../res/allies/thibault.png").convert_alpha())

        # Font
        self.font_name = "../res/hud/minecraftia.ttf"

    def print_text(self, text, size, x, y, max_width, center=False):
        """
        @summary Affiche un texte a l'ecran
        @param text: La String a afficher
        @param size: Taille en pixel du texte
        @param x: Position x
        @param y: Position y
        @param max_width: Taille maximale du texte avant de faire un retour a la ligne
        @param center: Centrer le texte (max_width inutile)
        """
        # Check si la police existe deja ou non
        if size in self.fonts_stock:
            font = self.fonts_stock[size]
        else:
            font = pygame.font.Font(self.font_name, int(size))
            self.fonts_stock[size] = font

        text_surface = font.render(text, 0, (255, 255, 255))
        width, max_height = text_surface.get_size()

        if center:
            self.window.blit(text_surface, (x - width // 2, y))
            return

        if width < max_width:  # Si nous avons assez de place on affiche la ligne sur sa ligne
            self.window.blit(text_surface, (x, y))
        else:  # Sinon, nous calculons des retours a la ligne
            pos_height = 0
            splitted_text = text.split()
            while len(splitted_text) > 0:
                text_temp = ""
                text_temp_printable = text_temp
                width = 0
                while width < max_width and len(splitted_text) > 0:
                    text_temp_printable = text_temp
                    text_temp += splitted_text.pop(0)
                    text_surface = font.render(text_temp, 0, (255, 255, 255))
                    width, height = text_surface.get_size()
                    text_temp += " "

                if width > max_width:
                    splitted_temp = text_temp.split()
                    # Si nous n'avons qu'un seul mot et qu'il depasse quand meme on affiche
                    if len(splitted_temp) == 1:
                        text_temp_printable = text_temp
                    else:  # sinon on ajoute le mot depassant a la ligne d'apres
                        splitted_text.insert(
                            0, splitted_temp[len(splitted_temp) - 1])
                else:
                    text_temp_printable = text_temp

                text_surface = font.render(
                    text_temp_printable, 0, (255, 255, 255))
                self.window.blit(text_surface, (x, y + pos_height))
                pos_height += int(max_height / 1.4)

    def print_clear(self):
        """
        @summary Vide l'ecran avec un ecran noir
        """
        pygame.draw.rect(self.window, (0, 0, 0),
                         (0, 0, self.wwidth, self.wheight))

    def print_room(self, room, char):
        """
        @summary Affiche la salle active a l'ecran
        @param room : salle a afficher
        @param char : personnage principal (pour avoir l'orientation de la salle)
        """
        doors = room.get_doors()
        orientation = char.get_orientation()

        # Portes et murs ont la meme taille niveau sprite
        tempx, tempy = self.wall_tiles[0].get_size()
        size_width, size_height = int(
            self.wwidth * 0.55), int(self.wwidth * 0.55 * tempy / tempx)

        # Choix d'affichage entre murs et portes
        if doors[(0 + orientation) % 4]:
            self.window.blit(pygame.transform.scale(
                self.door_tiles[5], (size_width, size_height)), (0, 0))
        else:
            self.window.blit(pygame.transform.scale(
                self.wall_tiles[5], (size_width, size_height)), (0, 0))
        if doors[(-1 + orientation) % 4]:
            self.window.blit(pygame.transform.scale(
                self.door_tiles[7], (size_width, size_height)), (0, 0))
        else:
            self.window.blit(pygame.transform.scale(
                self.wall_tiles[7], (size_width, size_height)), (0, 0))
        if doors[(1 + orientation) % 4]:
            self.window.blit(pygame.transform.scale(
                self.door_tiles[6], (size_width, size_height)), (0, 0))
        else:
            self.window.blit(pygame.transform.scale(
                self.wall_tiles[6], (size_width, size_height)), (0, 0))

        if room.is_exit():
            self.window.blit(pygame.transform.scale(self.ceiling_tiles[8 + orientation % 4], (size_width, size_height)),
                             (0, 0))
        else:
            self.window.blit(pygame.transform.scale(
                self.ceiling_tiles[7], (size_width, size_height)), (0, 0))

    def print_character(self, char):
        """
        @summary Affiche Un personnage (monstre / Marchand)
        @param char : personnage a afficher
        """
        tempx, tempy = self.monsters[0].get_size(
        )  # Les monstres ont la meme taille niveau sprite
        size_width, size_height = int(
            self.wwidth * 0.55), int(self.wwidth * 0.55 * tempy / tempx)

        sprite = None
        if isinstance(char, Monster):
            sprite = self.monsters
        elif isinstance(char, Merchant):
            sprite = self.merchants
        else:
            return  # Inconnu, on quitte sans afficher

        self.window.blit(pygame.transform.scale(
            sprite[char.icon_id], (size_width, size_height)), (0, 0))

    def print_reaction_icon(self, reaction, opacity, is_character=False):
        """
        @summary Affiche une icone de reaction
        @param reaction : reaction a afficher
        @param opacity : opacite de la reaction
        @param is_character : doit-on l'afficher sur le personnage principal?
        """

        if reaction >= 1:
            if is_character:
                tempx, tempy = self.active_equipment[0].get_size()
                size_width = self.wwidth * 0.22

                temp_surf = pygame.transform.scale(self.hud_icons[(reaction - 1) % len(self.hud_icons)],
                                                   (int(size_width), int(size_width)))
                temp_surf.set_alpha(int(opacity * 255))
                self.window.blit(
                    temp_surf, (int(self.wwidth * 0.77 - size_width // 8), int(self.wheight * 0.30)))

            else:
                tempx, tempy = self.monsters[0].get_size()
                size_width, size_height = int(
                    self.wwidth * 0.55 / 2), int(self.wwidth * 0.55 * tempy / tempx / 2)

                temp_surf = pygame.transform.scale(self.hud_icons[(reaction - 1) % len(self.hud_icons)],
                                                   (size_width, size_width))
                temp_surf.set_alpha(int(opacity * 255))
                self.window.blit(temp_surf, (size_width // 2,
                                             size_height - size_width // 2))

    def print_inventory(self, char, cursor):
        """
        @summary Affiche l'inventaire du joueur
        @param char : personnage dont on affiche l'inventaire
        @param cursor : curseur (2D) dans l'inventaire
        """

        temptx, tempty = self.inventory_tab[0].get_size()
        size_width, size_height = self.wwidth * \
            0.55, self.wwidth * 0.55 * tempty / temptx
        self.window.blit(pygame.transform.scale(
            self.inventory_tab[0], (int(size_width), int(size_height))), (0, 0))

        # Le curseur
        tempcx, tempcy = self.inventory_cursor[0].get_size()
        size_cursor_width, size_cursor_height = size_width * \
            tempcx / temptx, size_height * tempcy / tempty
        self.window.blit(
            pygame.transform.scale(self.inventory_cursor[0], (int(size_cursor_width), int(size_cursor_height))), (
                int((cursor[0] + 1) * size_width * 4 /
                    temptx + cursor[0] * size_cursor_width),
                int((cursor[1] + 1) * size_width * 4 / temptx + cursor[1] * size_cursor_height)))

        # Objets de l'inventaire
        inventory = char.inventory.items
        for i in range(0, len(inventory)):
            if inventory[i] is not None:
                self.window.blit(
                    pygame.transform.scale(self.items_tiles[inventory[i].get_icon_id()],
                                           (int(size_cursor_width), int(size_cursor_height))), (
                        int((i % 8 + 1) * size_width * 4 /
                            temptx + (i % 8) * size_cursor_width),
                        int((i // 8 + 1) * size_width * 4 / temptx + (i // 8) * size_cursor_height)))

    def print_active_tab(self, char, cursor=None):
        """
        @summary Affiche la barre active du joueur
        @param char : personnage dont on affiche la barre active
        @param cursor : curseur dans la barre active (non Necessaire)
        """
        # On recupere la position sous l'affichage de la zone principale
        tempx, tempy = self.wall_tiles[0].get_size()
        starty = self.wwidth * 0.55 * tempy / tempx + self.wheight * 0.01

        temptx, tempty = self.active_tab[0].get_size()
        size_width, size_height = self.wwidth * \
            0.35, self.wwidth * 0.35 * tempty / temptx
        self.window.blit(pygame.transform.scale(self.active_tab[0], (int(size_width), int(size_height))),
                         (self.wwidth * 0.60, starty))

        # Le curseur
        tempcx, tempcy = self.inventory_cursor[0].get_size()
        size_cursor_width, size_cursor_height = size_width * \
            tempcx / temptx, size_height * tempcy / tempty
        if cursor is not None:
            self.window.blit(
                pygame.transform.scale(self.inventory_cursor[0], (int(size_cursor_width), int(size_cursor_height))), (
                    int(self.wwidth * 0.60 + (cursor[0] + 1) * size_width * 22 / temptx + cursor[
                        0] * size_cursor_width),
                    int(starty + size_width * 4 / temptx + cursor[1] * (size_width * 22 / temptx + size_cursor_width))))

        # Logo d'attaque normale
        self.window.blit(
            pygame.transform.scale(self.items_tiles[items_id["attack_logo"]],
                                   (int(size_cursor_width), int(size_cursor_height))), (
                int(self.wwidth * 0.60 + size_width * 22 / temptx),
                int(starty + size_width * 4 / temptx)))

        # Sorts de la barre active
        spells = char.inventory.active_spells
        for i in range(1, 4):
            if spells[i - 1] is not None:
                self.window.blit(
                    pygame.transform.scale(self.items_tiles[spells[i - 1].get_icon_id()], (int(size_cursor_width),
                                                                                           int(size_cursor_height))), (
                        int(self.wwidth * 0.60 + (i + 1) * size_width *
                            22 / temptx + i * size_cursor_width),
                        int(starty + size_width * 4 / temptx)))

        # Consommables de la barre active
        usables = char.inventory.active_comsumable
        for i in range(0, 4):
            if usables[i] is not None:
                self.window.blit(
                    pygame.transform.scale(self.items_tiles[usables[i].get_icon_id()], (int(size_cursor_width),
                                                                                        int(size_cursor_height))), (
                        int(self.wwidth * 0.60 + (i + 1) * size_width *
                            22 / temptx + i * size_cursor_width),
                        int(starty + size_width * 4 / temptx + size_width * 22 / temptx + size_cursor_width)))

    def print_active_equipment(self, char):
        """
        @summary Affiche l'equipement actif du joueur
        @param char : personnage dont on affiche l'equipement
        """
        # On affiche la zone principale (les cases)
        tempx, tempy = self.active_equipment[0].get_size()
        size_width, size_height = self.wwidth * 0.22, self.wwidth * 0.22 * tempy / tempx
        self.window.blit(pygame.transform.scale(self.active_equipment[0], (int(size_width), int(size_height))),
                         (int(self.wwidth * 0.77), int(self.wheight * 0.30)))

        # Taille visuelle des objets
        tempix, tempiy = self.items_tiles[0].get_size()
        item_width, item_height = size_width * \
            tempix / tempx, size_height * tempiy / tempy

        # amulet
        if char.inventory.amulet is None:
            icon_id = items_id["no_amulet"]
        else:
            icon_id = char.inventory.amulet.get_icon_id()
        self.window.blit(
            pygame.transform.scale(
                self.items_tiles[icon_id], (int(item_width), int(item_height))),
            (int(self.wwidth * 0.77 + size_width * 4 / tempx),
             int(self.wheight * 0.30 + size_width * 4 / tempx)))
        # ring
        if char.inventory.ring is None:
            icon_id = items_id["no_ring"]
        else:
            icon_id = char.inventory.ring.get_icon_id()
        self.window.blit(
            pygame.transform.scale(
                self.items_tiles[icon_id], (int(item_width), int(item_height))),
            (int(self.wwidth * 0.77 + size_width * 4 / tempx),
             int(self.wheight * 0.30 + 3 * size_width * 4 / tempx + item_height)))
        # Helmet
        if char.inventory.helmet is None:
            icon_id = items_id["no_helmet"]
        else:
            icon_id = char.inventory.helmet.get_icon_id()
        self.window.blit(
            pygame.transform.scale(
                self.items_tiles[icon_id], (int(item_width), int(item_height))),
            (int(self.wwidth * 0.77 + 3 * size_width * 4 / tempx + item_width),
             int(self.wheight * 0.30 + size_width * 4 / tempx)))
        # Chest
        if char.inventory.chest is None:
            icon_id = items_id["no_chest"]
        else:
            icon_id = char.inventory.chest.get_icon_id()
        self.window.blit(
            pygame.transform.scale(
                self.items_tiles[icon_id], (int(item_width), int(item_height))),
            (int(self.wwidth * 0.77 + 3 * size_width * 4 / tempx + item_width),
             int(self.wheight * 0.30 + 3 * size_width * 4 / tempx + item_height)))
        # Legs
        if char.inventory.legs is None:
            icon_id = items_id["no_legs"]
        else:
            icon_id = char.inventory.legs.get_icon_id()
        self.window.blit(
            pygame.transform.scale(
                self.items_tiles[icon_id], (int(item_width), int(item_height))),
            (int(self.wwidth * 0.77 + 3 * size_width * 4 / tempx + item_width),
             int(self.wheight * 0.30 + 5 * size_width * 4 / tempx + 2 * item_height)))
        # Boots
        if char.inventory.boots is None:
            icon_id = items_id["no_boots"]
        else:
            icon_id = char.inventory.boots.get_icon_id()
        self.window.blit(
            pygame.transform.scale(
                self.items_tiles[icon_id], (int(item_width), int(item_height))),
            (int(self.wwidth * 0.77 + 3 * size_width * 4 / tempx + item_width),
             int(self.wheight * 0.30 + 7 * size_width * 4 / tempx + 3 * item_height)))
        # Gloves
        if char.inventory.gloves is None:
            icon_id = items_id["no_gloves"]
        else:
            icon_id = char.inventory.gloves.get_icon_id()
        self.window.blit(
            pygame.transform.scale(
                self.items_tiles[icon_id], (int(item_width), int(item_height))),
            (int(self.wwidth * 0.77 + 5 * size_width * 4 / tempx + 2 * item_width),
             int(self.wheight * 0.30 + 3 * size_width * 4 / tempx + item_height)))
        # Weapon
        if char.inventory.weapon is None:
            icon_id = items_id["no_weapon"]
        else:
            icon_id = char.inventory.weapon.get_icon_id()
        self.window.blit(
            pygame.transform.scale(
                self.items_tiles[icon_id], (int(item_width), int(item_height))),
            (int(self.wwidth * 0.77 + 7 * size_width * 4 / tempx + 3 * item_width),
             int(self.wheight * 0.30 + 5 * size_width * 4 / tempx + 2 * item_height)))
        # Shield
        if char.inventory.shield is None:
            icon_id = items_id["no_shield"]
        else:
            icon_id = char.inventory.shield.get_icon_id()
        self.window.blit(
            pygame.transform.scale(
                self.items_tiles[icon_id], (int(item_width), int(item_height))),
            (int(self.wwidth * 0.77 + 7 * size_width * 4 / tempx + 3 * item_width),
             int(self.wheight * 0.30 + 7 * size_width * 4 / tempx + 3 * item_height)))

    def print_map(self, carte: str = None) -> None:
        """
        @summary Affichage de la carte a l'ecran
        @param carte : str la map en text generé par plt
        """
        raw_data, size = carte
        surf = pygame.image.frombuffer(raw_data, size, "RGB")
        surf.set_colorkey((255, 255, 255))
        tempx, tempy = surf.get_size()
        size_width, size_height = int(
            self.wheight * 0.30 * tempx / tempy), int(self.wheight * 0.30)
        self.window.blit(pygame.transform.scale(surf, (size_width, size_height)),
                         (int(self.wwidth * 0.55), 0))

    def print_game_infos(self, char, actual_level):
        """
        @summary Affiche le niveau du joueur et l'etage du donjon
        @param char: Personnage
        """
        self.print_text("Pseudo  : " + str(char.name), self.wheight * 0.04, int(self.wwidth * 0.78),
                        int(self.wheight * 0.01), int(self.wwidth * 0.22))
        self.print_text("Etage  : " + str(actual_level), self.wheight * 0.04, int(self.wwidth * 0.78),
                        int(self.wheight * 0.11), int(self.wwidth * 0.22))
        self.print_text("Niveau : " + str(char.level), self.wheight * 0.04, int(self.wwidth * 0.78),
                        int(self.wheight * 0.20), int(self.wwidth * 0.22))

    def print_description(self, item: Item) -> None:
        """
        @summary Affiche la description d'un objet par dessus la carte
        @param item: Objet dont on note la description
        """
        tempx, tempy = self.description_tiles[0].get_size()
        size_width, size_height = int(
            self.wheight * 0.30 * tempx / tempy), int(self.wheight * 0.30)
        self.window.blit(pygame.transform.scale(self.description_tiles[0], (size_width, size_height)),
                         (int(self.wwidth * (0.55 + 0.45 / 2) - size_width / 2), 0))

        if item is not None:
            self.print_gold(item.prix, int(
                self.wwidth * (0.55 + 0.45 / 2) - size_width / 4), 15, False)
        """if isinstance(item, Armor):
            self.window.blit(pygame.transform.scale(self.description_tiles[0], (size_width, size_height)),
                             (int(self.wwidth * (0.55 + 0.45 / 2) - size_width / 2), 0))
            self.print_text()
        """
        # TODO les différents types d'objets

    def print_pseudo_max_size(self, pseudo):
        """
        @summary Affiche le pseudo de la personne au milieu de l'ecran
        @param pseudo: pseudo a afficher
        """
        self.print_text(pseudo, self.wheight // 20, self.wwidth //
                        2, self.wheight // 2, self.wwidth, True)
        self.print_text("Entrez votre Pseudo", self.wheight // 10,
                        self.wwidth // 2, self.wheight // 4, self.wwidth, True)

    def print_info_on_menu(self, dicttoprint: dict, title: str = None) -> None:
        """
        @summary Affiche la description d'un objet par dessus la carte
        @param dicttoprint: dictionnaire des infos a afficher
        @param title: Titre éventuel
        """
        tempx, tempy = self.description_tiles[0].get_size()
        size_width, size_height = int(
            self.wheight * 0.60 * tempx / tempy), int(self.wheight * 0.90)
        self.window.blit(pygame.transform.scale(self.description_tiles[0], (size_width, size_height)),
                         (int(self.wwidth * 0.7 - size_width / 2), self.wheight // 40))
        if title is not None:
            self.print_text(title, size_height//15,
                            int(self.wwidth * 0.7 - size_width //
                                2 + size_width // 20),
                            self.wheight // 20 * 2,
                            self.wwidth // 2)

        if isinstance(dicttoprint, dict):
            for i, m in enumerate(dicttoprint):
                self.print_text(m + " : " + str(dicttoprint[m]), size_height // 25,
                                self.wwidth//100 * 48,
                                self.wheight // 7 + size_height // 21 * (1+i),
                                self.wwidth//2)

    def resize_event(self, event):
        """
        @summary fonction gerant la modification de la taille de la fenetre de jeu
        @param event : evenement genere par pygame
        """
        width, height = event.size
        if width / height != 16 / 9:
            height = (width * 9) // 16
        self.window = pygame.display.set_mode((width, height), RESIZABLE)
        self.wwidth, self.wheight = pygame.display.get_surface().get_size()
        self.parallax_scaled = []
        for i in range(0, len(self.parallax)):
            self.parallax_scaled.append(pygame.transform.scale(
                self.parallax[i], (self.wwidth * 2, self.wheight)))

    def print_parallax_background(self, position):
        """
        @summary Affiche le fond style parallax
        @param position : index du parallax
        """
        tempx, tempy = self.cases_hud[0].get_size()
        coeff = tempx / tempy * self.wwidth * 0.0001
        for i in range(0, len(self.parallax_scaled)):
            self.window.blit(self.parallax_scaled[i], (int(
                0 - (i * coeff * position % self.wwidth)), 0))

    def print_cases_menu(self, cursor, in_game=False):
        """
        @summary Affiche l'HUD presentant les options du menu (Nouvelle partie, charger, Achievements...)
        @param cursor : Curseur pointant la case active
        @param in_game: Si nous sommes dans une partie en cours
        """
        tempx, tempy = self.cases_hud[0].get_size()
        size_width, size_height = int(
            self.wwidth * 0.28), int(self.wwidth * 0.28 * tempy / tempx)

        texts = ["Nouvelle Partie", "Charger Partie", "Succes", "Statistiques"] if not in_game else ["Continuer",
                                                                                                     "Sauvegarder",
                                                                                                     "Succes",
                                                                                                     "Statistiques"]

        for i in range(0, 4):
            hovered = 1 if cursor == i else 0

            self.window.blit(pygame.transform.scale(self.cases_hud[hovered + 2], (size_width, size_height)),
                             (self.wwidth * 0.02, int(self.wheight * 0.20 + self.wheight * 0.15 * i)))
            # On centre le texte sur la case et on met une taille maximale de 0 (comme on centre ca ne change rien)
            self.print_text(texts[i], int(size_height // 3), size_width // 2 + self.wwidth * 0.02,
                            int(self.wheight * 0.20 + self.wheight * 0.15 * i) + size_height // 4, 0, True)

    def print_case(self, cursor, position, text):
        """
        @summary Affiche une case de l'HUD
        @param cursor: Position du curseur (== position si sur cette case)
        @param position: Position de la case (par rapport a la premiere == 0)
        @param text: texte dans la case (si text = "<^>" on affiche les fleches)
        """
        tempx, tempy = self.cases_hud[0].get_size()
        size_width, size_height = int(
            self.wwidth * 0.20), int(self.wwidth * 0.20 * tempy / tempx)

        hovered = 1 if cursor == position else 0

        # Cases fleches
        if text == "<^>":
            self.window.blit(pygame.transform.scale(self.cases_hud[hovered], (size_width, size_height)),
                             (int(self.wwidth * 0.56), int(self.wheight * 0.30 + self.wheight * 0.08 * position)))
        else:
            self.window.blit(pygame.transform.scale(self.cases_hud[hovered + 2], (size_width, size_height)),
                             (int(self.wwidth * 0.56), int(self.wheight * 0.30 + self.wheight * 0.08 * position)))
            # On centre le texte sur la case et on met une taille maximale de 0 (comme on centre ca ne change rien)
            self.print_text(text, int(size_height // 2.5), int(self.wwidth * 0.56) + size_width // 2,
                            int(self.wheight * 0.30 + self.wheight * 0.08 * position) + size_height // 4, 0, True)

    def print_cases_hud(self, cursor, situation=0):
        """
        @summary Affiche l'HUD presentant les options en mode exploration / Inventaire / ... (fleches, inventaire ...)
        @param cursor : Curseur pointant la case active
        @param situation : Situation des cases:
                0-Exploration,
                1-Sortie de donjon,
                2-Marchand,
                3-Action Equipement(armures,armes,sorts),
                4-Action consommables
        """

        if situation == 0:  # Exploration
            self.print_case(cursor, 0, "<^>")
            self.print_case(cursor, 1, "Inventaire")
            self.print_case(cursor, 2, "Sauvegarder")
        elif situation == 1:  # Exploration Fin Donjon
            self.print_case(cursor, 0, "<^>")
            self.print_case(cursor, 1, "Inventaire")
            self.print_case(cursor, 2, "Sauvegarder")
            self.print_case(cursor, 3, "Descendre")
        elif situation == 2:  # Exploration Marchand
            self.print_case(cursor, 0, "<^>")
            self.print_case(cursor, 1, "Inventaire")
            self.print_case(cursor, 2, "Sauvegarder")
            self.print_case(cursor, 3, "Acheter")
            self.print_case(cursor, 4, "Vendre")
        elif situation == 3:  # Inventaire Action Objet
            self.print_case(cursor, 0, "Equiper")
            self.print_case(cursor, 1, "Jeter")
        elif situation == 4:  # Inventaire Action Consommables
            self.print_case(cursor, 0, "Equiper")
            self.print_case(cursor, 1, "Jeter")
            self.print_case(cursor, 2, "Utiliser")

    def print_numbers(self, number, is_percent, width, height, posx, posy):
        """
        @summary Affiche un nombre (positif entier) a l'ecran
        @summary (en pourcentages ou non, auquel cas il est fixe a gauche de la position)
        @param number: Nombre a affiche
        @param is_percent: Mets-on un pourcentage au bout du nombre
        @param width: epaisseur des chiffres
        @param height: hauteur des chiffres
        @param posx: position x du nombre (droite si pourcentage)
        @param posy: position y du nombre (Toujours en haut des sprites)
        """
        number = int(number)
        letters = []  # Chiffres a affiche un a un
        if number == 0:
            letters.insert(0, 0)
        else:
            while number > 0:
                letters.insert(0, number % 10)
                number = number // 10

        for i in range(0, len(letters)):
            if is_percent:
                self.window.blit(pygame.transform.scale(self.numbers_tiles[letters[len(letters) - 1 - i]],
                                                        (int(width), int(height))),
                                 (int(posx - width * (i + 2)), int(posy)))
            else:
                self.window.blit(pygame.transform.scale(self.numbers_tiles[letters[i]], (int(width), int(height))),
                                 (int(posx + width * i), int(posy)))
        if is_percent:
            self.window.blit(pygame.transform.scale(self.numbers_tiles[10], (int(width), int(height))),
                             (int(posx - width), int(posy)))

    def print_gold(self, price, x, y, limited=False):
        """
        @summary Affiche un prix
        @param price : Prix a afficher
        @param x : position x
        @param y : position y
        @param limited : Doit-on raccourcir le prix ? (auquel cas il est centre)
        """
        tempx, tempy = self.items_tiles[items_id["gold"]].get_size()
        size_width, size_height = self.wheight * \
            0.07 * tempx / tempy, self.wheight * 0.07

        self.window.blit(
            pygame.transform.scale(
                self.items_tiles[items_id["gold"]], (int(size_width), int(size_height))),
            (int(x - size_width if not limited else x - size_width / 2),
             int(y if not limited else y - size_height)))

        price = int(price)
        unit = [".", "K", "M", "G", "T", "P", "E", "Z", "Y", "*"]
        index_unit = 0
        while price > price % 1000:
            price = price // 1000
            if index_unit < len(unit) - 1:
                index_unit += 1

        self.print_text(str(
            price) + unit[index_unit], size_height * 0.75, int(x), int(y), self.wwidth, limited)

    def print_fillers(self, char, armoring=False, monster=False):
        """
        @summary Affichage des fillers (Vie, Mana, Armure)
        @param char : Personnage selon lequel on affiche les fillers
        @param armoring : Remplace t on la barre d'experience par une barre de shield?
        @param monster : Est-ce que nous affichons les stats des mobs ?
        """
        if armoring:
            percentages = [char.get_life_percent(
            ), char.get_mana_percent(), char.get_armor_percent()]
            plain_numbers = [char.get_health(), char.get_mana(),
                             char.get_armor()]
        else:
            percentages = [char.get_life_percent(
            ), char.get_mana_percent(), char.get_experience_percent()]
            plain_numbers = [char.get_health(), char.get_mana(),
                             char.get_experience()]
        for i in range(0, len(percentages)):
            if percentages[i] < 0:
                percentages[i] = 0
        for i in range(0, len(plain_numbers)):
            if plain_numbers[i] < 0:
                plain_numbers[i] = 0

        # On recupere la position sous l'affichage de la zone principale (ou a droite si c'est un monstre)
        tempx, tempy = self.wall_tiles[0].get_size()
        if monster:
            starty = self.wheight * 0.05
            startx = self.wwidth * 0.56
            coef = 0.75
        else:
            starty = self.wwidth * 0.55 * tempy / tempx
            startx = 0
            coef = 1

        # Fills Main
        tempx_main, tempy_main = self.fills_main[0].get_size()
        size_width_main = coef * self.wheight * 0.25 * tempx_main / tempy_main
        size_height_main = coef * self.wheight * 0.25

        self.window.blit(pygame.transform.scale(self.fills_main[char.get_orientation() % 4 if not monster else 4],
                                                (int(size_width_main), int(size_height_main))),
                         (startx, int(starty + coef * self.wheight * 0.01)))
        if not monster:
            self.print_gold(char.inventory.money, startx + size_width_main * 0.375,
                            starty + coef * self.wheight * 0.01 + size_height_main * 0.4, True)

        # Fills Tubes
        size_width_tubes = coef * \
            (self.wwidth * 0.55 - self.wwidth * 0.055) - size_width_main
        size_height_tubes = coef * self.wheight * 0.25 * 0.25

        for i in range(0, 3):
            self.window.blit(
                pygame.transform.scale(self.fills_tubes[0], (int(size_width_tubes), int(size_height_tubes))), (
                    int(startx + size_width_main),
                    int(starty + coef * (
                        self.wheight * 0.01) + (5 * size_height_main / 16) * i + size_height_main / 16)))

        # Fills Filler
        size_height_filler = size_height_tubes * 14 / 16
        for i in range(0, 3):
            size_width_filler = min(
                percentages[i] * size_width_tubes, size_width_tubes)
            if armoring and i == 2:  # On saute le 2 pour afficher l'armure (3)
                index = 3
            else:
                index = i
            self.window.blit(
                pygame.transform.scale(self.fills_fillers[index], (int(size_width_filler), int(size_height_filler))), (
                    int(startx + size_width_main), int(starty + coef * (self.wheight * 0.01) + size_height_main / 16 + (
                        5 * size_height_main / 16) * i + size_height_main / 64)))

        # Fills Tips
        size_width_tips, size_height_tips = size_width_main * \
            32 / 84, size_height_main * 20 / 64
        for i in range(0, 3):
            if armoring and i == 2:  # On saute le 2 pour afficher l'armure (3)
                index = 3
            else:
                index = i
            self.window.blit(
                pygame.transform.scale(self.fills_tips[index], (int(
                    size_width_tips), int(size_height_tips))),
                (int(startx + size_width_main + size_width_tubes), int(
                    starty + coef * (self.wheight * 0.01) + size_height_main / 32 + size_height_main * 20 / 64 * i)))

        # Numbers Percents
        size_width_number, size_height_number = size_width_main * \
            11 / 84, size_height_main * 11 / 64
        for i in range(0, 3):
            self.print_numbers(percentages[i] * 100, True, size_width_number, size_height_number,
                               startx + size_width_main + size_width_tubes,
                               starty + coef * (self.wheight * 0.01) + size_height_main / 16 + (
                5 * size_height_main / 16) * i + size_height_main / 32)
        # Numbers Plain
        for i in range(0, 3):
            self.print_numbers(plain_numbers[i], False, size_width_number, size_height_number, startx + size_width_main,
                               starty + coef * (self.wheight * 0.01) + size_height_main / 16 + (
                5 * size_height_main / 16) * i + size_height_main / 32)
