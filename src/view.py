import pygame
from pygame.locals import RESIZABLE


def load_tile_table(filename, nbx: int, nby: int):
    """
    @brief Charge un spritesheet selon une image et le nombre de sprites
    @param filename : nom du fichier
    @param nbx : nombre de sprites horizontaux
    @param nby : nombre de sprites verticaux
    @return : un tableau de surfaces contenant les sprites
    """
    image = pygame.image.load(filename).convert_alpha()
    image_width, image_height = image.get_size()
    tile_table = []

    for tile_y in range(0, nby):
        for tile_x in range(0, nbx):
            rect = (tile_x * image_width // nbx, tile_y * image_height // nby, image_width // nbx, image_height // nby)
            tile_table.append(image.subsurface(rect))
    return tile_table


class View:
    items_id = {
        "error": 77,
        "no_helmet": 0,
        "no_chest": 1,
        "no_legs": 2,
        "no_boots": 3,
        "no_gloves": 4,
        "no_bracelet": 5,
        "no_amulet": 6,
        "no_weapon": 7,
        "no_shield": 8,
        "attack_logo": 78,
        "amulet1": 9,
        "amulet2": 19,
        "amulet3": 29
    }

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
    # Assets Monsters
    monsters = []
    # Font
    font_name = None
    fonts_stock = {}
    # Stock les polices selon leurs tailles
    # #(evite de reouvrir la police chaque fois que l'on reecri a la meme taille)

    def __init__(self) -> None:
        # Creation de la fenetre
        self.window = pygame.display.set_mode((800, 450), RESIZABLE)
        self.wwidth, self.wheight = pygame.display.get_surface().get_size()

        self.load_assets()

    def load_assets(self):
        """
        @brief Charge les sprites necessaires au bon fonctionnement du jeu
        """
        # Assets
        self.wall_tiles = load_tile_table("res/tiles/dungeon_wall.png", 4, 4)
        self.door_tiles = load_tile_table("res/tiles/dungeon_door.png", 4, 4)
        self.ceiling_tiles = load_tile_table("res/tiles/dungeon_ceiling.png", 4, 4)
        self.cases_hud = load_tile_table("res/hud/cases.png", 1, 12)
        self.fills_fillers = load_tile_table("res/hud/fills_fillers.png", 1, 3)
        self.fills_tips = load_tile_table("res/hud/fills_tips.png", 1, 3)
        self.fills_main = load_tile_table("res/hud/fills_main.png", 4, 1)
        self.fills_tubes = load_tile_table("res/hud/fills_tubes.png", 1, 1)
        self.numbers_tiles = load_tile_table("res/hud/numbers.png", 11, 1)
        self.inventory_tab = load_tile_table("res/inventory/inventory_tab.png", 1, 1)
        self.inventory_cursor = load_tile_table("res/inventory/inventory_cursor.png", 1, 1)
        self.active_tab = load_tile_table("res/inventory/active_tab.png", 1, 1)
        self.active_equipment = load_tile_table("res/inventory/active_equipment.png", 1, 1)
        self.items_tiles = load_tile_table("res/inventory/items.png", 10, 8)

        # Assets Monsters
        self.monsters.append(pygame.image.load("res/enemies/druid.png").convert_alpha())
        self.monsters.append(pygame.image.load("res/enemies/imp.png").convert_alpha())
        self.monsters.append(pygame.image.load("res/enemies/mimic.png").convert_alpha())
        self.monsters.append(pygame.image.load("res/enemies/skeleton.png").convert_alpha())
        self.monsters.append(pygame.image.load("res/enemies/zombie.png").convert_alpha())

        # Font
        self.font_name = "res/hud/minecraftia.ttf"

    def print_text(self, text, size, x, y, max_width):
        """
        @brief Affiche un texte a l'ecran
        :param text: La String a afficher
        :param size: Taille en pixel du texte
        :param x: Position x
        :param y: Position y
        :param max_width: Taille maximale du texte avant de faire un retour a la ligne
        """
        # Check si la police existe deja ou non
        if size in self.fonts_stock:
            font = self.fonts_stock[size]
        else:
            font = pygame.font.Font(self.font_name, size)
            self.fonts_stock[size] = font

        text_surface = font.render(text, 0, (255, 255, 255))
        width, max_height = text_surface.get_size()
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
                    if len(splitted_temp) == 1:  # Si nous n'avons qu'un seul mot et qu'il depasse quand meme on affiche
                        text_temp_printable = text_temp
                    else:  # sinon on ajoute le mot depassant a la ligne d'apres
                        splitted_text.insert(0, splitted_temp[len(splitted_temp) - 1])

                text_surface = font.render(text_temp_printable, 0, (255, 255, 255))
                self.window.blit(text_surface, (x, y + pos_height))
                pos_height += max_height

    def print_clear(self):
        """
        @brief Vide l'ecran avec un ecran noir
        """
        pygame.draw.rect(self.window, (0, 0, 0), (0, 0, self.wwidth, self.wheight))

    def print_room(self, room, char):
        """
        @brief Affiche la salle active a l'ecran
        @param room : salle a afficher
        @param char : personnage principal (pour avoir l'orientation de la salle)
        """
        doors = room.get_doors()
        orientation = char.get_orientation()

        tempx, tempy = self.wall_tiles[0].get_size()  # Portes et murs ont la meme taille niveau sprite
        size_width, size_height = int(self.wwidth * 0.55), int(self.wwidth * 0.55 * tempy / tempx)

        # Choix d'affichage entre murs et portes
        if doors[(0 + orientation) % 4]:
            self.window.blit(pygame.transform.scale(self.door_tiles[5], (size_width, size_height)), (0, 0))
        else:
            self.window.blit(pygame.transform.scale(self.wall_tiles[5], (size_width, size_height)), (0, 0))
        if doors[(-1 + orientation) % 4]:
            self.window.blit(pygame.transform.scale(self.door_tiles[7], (size_width, size_height)), (0, 0))
        else:
            self.window.blit(pygame.transform.scale(self.wall_tiles[7], (size_width, size_height)), (0, 0))
        if doors[(1 + orientation) % 4]:
            self.window.blit(pygame.transform.scale(self.door_tiles[6], (size_width, size_height)), (0, 0))
        else:
            self.window.blit(pygame.transform.scale(self.wall_tiles[6], (size_width, size_height)), (0, 0))

        if room.is_exit():
            self.window.blit(pygame.transform.scale(self.ceiling_tiles[8 + orientation % 4], (size_width, size_height)),
                             (0, 0))
        else:
            self.window.blit(pygame.transform.scale(self.ceiling_tiles[7], (size_width, size_height)), (0, 0))

    def print_monster(self, char):
        tempx, tempy = self.monsters[0].get_size()  # Les monstres ont la meme taille niveau sprite
        size_width, size_height = int(self.wwidth * 0.55), int(self.wwidth * 0.55 * tempy / tempx)

        self.window.blit(pygame.transform.scale(self.monsters[char.icon_id], (size_width, size_height)), (0, 0))

    def print_inventory(self, char, cursor):
        """
        @brief Affiche l'inventaire du joueur
        @param char : personnage dont on affiche l'inventaire
        @param cursor : curseur (2D) dans l'inventaire
        """

        temptx, tempty = self.inventory_tab[0].get_size()
        size_width, size_height = self.wwidth * 0.55, self.wwidth * 0.55 * tempty / temptx
        self.window.blit(pygame.transform.scale(self.inventory_tab[0], (int(size_width), int(size_height))), (0, 0))

        # Le curseur
        tempcx, tempcy = self.inventory_cursor[0].get_size()
        size_cursor_width, size_cursor_height = size_width * tempcx / temptx, size_height * tempcy / tempty
        self.window.blit(
            pygame.transform.scale(self.inventory_cursor[0], (int(size_cursor_width), int(size_cursor_height))), (
                int((cursor[0] + 1) * size_width * 4 / temptx + cursor[0] * size_cursor_width),
                int((cursor[1] + 1) * size_width * 4 / temptx + cursor[1] * size_cursor_height)))

        # Objets de l'inventaire
        inventory = char.get_inventory()
        for i in range(0, len(inventory)):
            self.window.blit(
                pygame.transform.scale(self.items_tiles[inventory[i].get_icon_id],
                                       (int(size_cursor_width), int(size_cursor_height))), (
                    int((i % 8 + 1) * size_width * 4 / temptx + (i % 8) * size_cursor_width),
                    int((i // 8 + 1) * size_width * 4 / temptx + (i // 8) * size_cursor_height)))

    def print_active_tab(self, char, cursor=None):
        """
        @brief Affiche la barre active du joueur
        @param char : personnage dont on affiche la barre active
        @param cursor : curseur dans la barre active (non Necessaire)
        """
        # On recupere la position sous l'affichage de la zone principale
        tempx, tempy = self.wall_tiles[0].get_size()
        starty = self.wwidth * 0.55 * tempy / tempx + self.wheight * 0.01

        temptx, tempty = self.active_tab[0].get_size()
        size_width, size_height = self.wwidth * 0.35, self.wwidth * 0.35 * tempty / temptx
        self.window.blit(pygame.transform.scale(self.active_tab[0], (int(size_width), int(size_height))),
                         (self.wwidth * 0.60, starty))

        # Le curseur
        tempcx, tempcy = self.inventory_cursor[0].get_size()
        size_cursor_width, size_cursor_height = size_width * tempcx / temptx, size_height * tempcy / tempty
        if cursor is not None:
            self.window.blit(
                pygame.transform.scale(self.inventory_cursor[0], (int(size_cursor_width), int(size_cursor_height))), (
                    int(self.wwidth * 0.60 + (cursor[0] + 1) * size_width * 22 / temptx + cursor[
                        0] * size_cursor_width),
                    int(starty + size_width * 4 / temptx + cursor[1] * (size_width * 22 / temptx + size_cursor_width))))

        # Logo d'attaque normale
        self.window.blit(
            pygame.transform.scale(self.items_tiles[self.items_id["attack_logo"]], (int(size_cursor_width), int(size_cursor_height))), (
                int(self.wwidth * 0.60 + size_width * 22 / temptx),
                int(starty + size_width * 4 / temptx)))

        # Sorts de la barre active
        spells = char.inventory.active_spells
        for i in range(1, 4):
            if spells[i-1] is not None:
                self.window.blit(
                    pygame.transform.scale(self.items_tiles[spells[i-1].get_icon_id()], (int(size_cursor_width), int(size_cursor_height))), (
                        int(self.wwidth * 0.60 + (i + 1) * size_width * 22 / temptx + i * size_cursor_width),
                        int(starty + size_width * 4 / temptx)))

        # Consommables de la barre active
        usables = char.inventory.active_comsumable
        for i in range(0, 4):
            if usables[i] is not None:
                self.window.blit(
                    pygame.transform.scale(self.items_tiles[usables[i].get_icon_id()], (int(size_cursor_width), int(size_cursor_height))), (
                        int(self.wwidth * 0.60 + (i + 1) * size_width * 22 / temptx + i * size_cursor_width),
                        int(starty + size_width * 4 / temptx + size_width * 22 / temptx + size_cursor_width)))

    def print_active_equipment(self, char):
        """
        @brief Affiche l'equipement actif du joueur
        @param char : personnage dont on affiche l'equipement
        """
        # On affiche la zone principale (les cases)
        tempx, tempy = self.active_equipment[0].get_size()
        size_width, size_height = self.wwidth * 0.22, self.wwidth * 0.22 * tempy / tempx
        self.window.blit(pygame.transform.scale(self.active_equipment[0], (int(size_width), int(size_height))),
                         (int(self.wwidth * 0.77), int(self.wheight * 0.30)))

        # Taille visuelle des objets
        tempix, tempiy = self.items_tiles[0].get_size()
        item_width, item_height = size_width * tempix / tempx, size_height * tempiy / tempy

        id = 0
        # Jewel1
        if char.inventory.jewel1 is None:
            id = self.items_id["no_amulet"]
        else:
            id = char.inventory.jewel1.get_icon_id
        self.window.blit(
            pygame.transform.scale(self.items_tiles[id], (int(item_width), int(item_height))),
            (int(self.wwidth * 0.77 + size_width * 4 / tempx),
             int(self.wheight * 0.30 + size_width * 4 / tempx)))
        # Jewel2
        if char.inventory.jewel2 is None:
            id = self.items_id["no_amulet"]
        else:
            id = char.inventory.jewel2.get_icon_id
        self.window.blit(
            pygame.transform.scale(self.items_tiles[id], (int(item_width), int(item_height))),
            (int(self.wwidth * 0.77 + size_width * 4 / tempx),
             int(self.wheight * 0.30 + 3 * size_width * 4 / tempx + item_height)))
        # Helmet
        if char.inventory.helmet is None:
            id = self.items_id["no_helmet"]
        else:
            id = char.inventory.helmet.get_icon_id
        self.window.blit(
            pygame.transform.scale(self.items_tiles[id], (int(item_width), int(item_height))),
            (int(self.wwidth * 0.77 + 3 * size_width * 4 / tempx + item_width),
             int(self.wheight * 0.30 + size_width * 4 / tempx)))
        # Chest
        if char.inventory.chest is None:
            id = self.items_id["no_chest"]
        else:
            id = char.inventory.chest.get_icon_id
        self.window.blit(
            pygame.transform.scale(self.items_tiles[id], (int(item_width), int(item_height))),
            (int(self.wwidth * 0.77 + 3 * size_width * 4 / tempx + item_width),
             int(self.wheight * 0.30 + 3 * size_width * 4 / tempx + item_height)))
        # Legs
        if char.inventory.legs is None:
            id = self.items_id["no_legs"]
        else:
            id = char.inventory.legs.get_icon_id
        self.window.blit(
            pygame.transform.scale(self.items_tiles[id], (int(item_width), int(item_height))),
            (int(self.wwidth * 0.77 + 3 * size_width * 4 / tempx + item_width),
             int(self.wheight * 0.30 + 5 * size_width * 4 / tempx + 2 * item_height)))
        # Boots
        if char.inventory.boots is None:
            id = self.items_id["no_boots"]
        else:
            id = char.inventory.boots.get_icon_id
        self.window.blit(
            pygame.transform.scale(self.items_tiles[id], (int(item_width), int(item_height))),
            (int(self.wwidth * 0.77 + 3 * size_width * 4 / tempx + item_width),
             int(self.wheight * 0.30 + 7 * size_width * 4 / tempx + 3 * item_height)))
        # Gloves
        if char.inventory.gloves is None:
            id = self.items_id["no_gloves"]
        else:
            id = char.inventory.gloves.get_icon_id
        self.window.blit(
            pygame.transform.scale(self.items_tiles[id], (int(item_width), int(item_height))),
            (int(self.wwidth * 0.77 + 5 * size_width * 4 / tempx + 2 * item_width),
             int(self.wheight * 0.30 + 3 * size_width * 4 / tempx + item_height)))
        # Weapon
        if char.inventory.weapon is None:
            id = self.items_id["no_weapon"]
        else:
            id = char.inventory.weapon.get_icon_id
        self.window.blit(
            pygame.transform.scale(self.items_tiles[id], (int(item_width), int(item_height))),
            (int(self.wwidth * 0.77 + 7 * size_width * 4 / tempx + 3 * item_width),
             int(self.wheight * 0.30 + 5 * size_width * 4 / tempx + 2 * item_height)))
        # Weapon
        if char.inventory.shield is None:
            id = self.items_id["no_shield"]
        else:
            id = char.inventory.shield.get_icon_id
        self.window.blit(
            pygame.transform.scale(self.items_tiles[id], (int(item_width), int(item_height))),
            (int(self.wwidth * 0.77 + 7 * size_width * 4 / tempx + 3 * item_width),
             int(self.wheight * 0.30 + 7 * size_width * 4 / tempx + 3 * item_height)))

    def print_map(self, map: str = None):
        """
        @brief Affichage de la map a l'ecran
        """
        raw_data, size = map
        surf = pygame.image.frombuffer(raw_data, size, "RGB")
        surf.set_colorkey((255, 255, 255))
        tempx, tempy = surf.get_size()
        size_width, size_height = int(self.wheight * 0.30 * tempx / tempy), int(self.wheight * 0.30)
        self.window.blit(pygame.transform.scale(surf, (size_width, size_height)),
                         (int(self.wwidth * (0.55 + 0.45 / 2) - size_width / 2), 0))

    def print_description(self, item):
        """
        @brief Affiche la description d'un objet par dessus la map
        :param item: Objet dont on note la description
        """
        i = 1

    def resize_event(self, event):
        """
        @brief fonction gerant la modification de la taille de la fenetre de jeu
        @param event : evenement genere par pygame
        """
        width, height = event.size
        if width / height != 16 / 9:
            height = (width * 9) // 16
        self.window = pygame.display.set_mode((width, height), RESIZABLE)
        self.wwidth, self.wheight = pygame.display.get_surface().get_size()

    def print_cases_hud(self, cursor, exit_case=False, merchant_case=False):
        """
        @brief Affiche l'HUD presentant les options en mode exploration (fleches, inventaire ...)
        @param cursor : Curseur pointant la case active
        @param exit_case : Ajout de la case Sortie de dongeon
        @param cursor : Ajout de la case commerce
        """
        tempx, tempy = self.cases_hud[0].get_size()
        size_width, size_height = int(self.wwidth * 0.20), int(self.wwidth * 0.20 * tempy / tempx)

        # Cases fleches
        if cursor == 0:
            self.window.blit(pygame.transform.scale(self.cases_hud[1], (size_width, size_height)),
                             (int(self.wwidth * 0.56), int(self.wheight * 0.30)))
        else:
            self.window.blit(pygame.transform.scale(self.cases_hud[0], (size_width, size_height)),
                             (int(self.wwidth * 0.56), int(self.wheight * 0.30)))

        # Cases inventaire et sauvegarde (toujours présents)
        for i in range(0, 2):
            if cursor == i + 1:
                self.window.blit(pygame.transform.scale(self.cases_hud[i * 2 + 3], (size_width, size_height)),
                                 (int(self.wwidth * 0.56), int(self.wheight * 0.30 + self.wheight * 0.08 * (i + 1))))
            else:
                self.window.blit(pygame.transform.scale(self.cases_hud[i * 2 + 2], (size_width, size_height)),
                                 (int(self.wwidth * 0.56), int(self.wheight * 0.30 + self.wheight * 0.08 * (i + 1))))

        if exit_case or merchant_case:
            i = 0
            if exit_case:
                i = 0
            elif merchant_case:
                i = i
            if cursor == 3:
                self.window.blit(pygame.transform.scale(self.cases_hud[i * 2 + 7], (size_width, size_height)),
                                 (int(self.wwidth * 0.56), int(self.wheight * 0.30 + self.wheight * 0.08 * 3)))
            else:
                self.window.blit(pygame.transform.scale(self.cases_hud[i * 2 + 6], (size_width, size_height)),
                                 (int(self.wwidth * 0.56), int(self.wheight * 0.30 + self.wheight * 0.08 * 3)))

    def print_numbers(self, number, is_percent, width, height, posx, posy):
        """
        @brief Affiche un nombre (positif entier) a l'ecran (en pourcentages ou non, auquel cas il est fixe a gauche de la position)
        :param number: Nombre a affiche
        :param is_percent: Mets-on un pourcentage au bout du nombre
        :param width: epaisseur des chiffres
        :param height: hauteur des chiffres
        :param posx: position x du nombre (droite si pourcentage)
        :param posy: position y du nombre (Toujours en haut des sprites)
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

    def print_fillers(self, char=None):
        """
        @brief Affichage des fillers (Vie, Mana, Armure)
        @param char : Personnage selon lequel on affiche les fillers
        """
        percentages = [char.get_life_percent(), char.get_mana_percent(), char.get_experience_percent()]
        for i in range(0, len(percentages)):
            if percentages[i] < 0:
                percentages[i] = 0
        plain_numbers = [char.get_health(), char.get_mana(), char.get_experience()]

        # On recupere la position sous l'affichage de la zone principale
        tempx, tempy = self.wall_tiles[0].get_size()
        starty = self.wwidth * 0.55 * tempy / tempx

        # Fills Main
        tempx_main, tempy_main = self.fills_main[0].get_size()
        size_width_main, size_height_main = self.wheight * 0.25 * tempx_main / tempy_main, self.wheight * 0.25
        self.window.blit(pygame.transform.scale(self.fills_main[char.get_orientation() % 4],
                                                (int(size_width_main), int(size_height_main))),
                         (0, int(starty + self.wheight * 0.01)))

        # Fills Tubes
        size_width_tubes, size_height_tubes = self.wwidth * 0.55 - size_width_main - self.wwidth * 0.055, self.wheight * 0.25 * 0.25
        for i in range(0, 3):
            self.window.blit(
                pygame.transform.scale(self.fills_tubes[0], (int(size_width_tubes), int(size_height_tubes))), (
                    int(size_width_main),
                    int(starty + self.wheight * 0.01 + size_height_main / 16 + (5 * size_height_main / 16) * i)))

        # Fills Filler
        size_height_filler = size_height_tubes * 14 / 16
        for i in range(0, 3):
            size_width_filler = percentages[i] * size_width_tubes
            self.window.blit(
                pygame.transform.scale(self.fills_fillers[i], (int(size_width_filler), int(size_height_filler))), (
                    int(size_width_main), int(starty + self.wheight * 0.01 + size_height_main / 16 + (
                            5 * size_height_main / 16) * i + size_height_main / 64)))

        # Fills Filler
        size_width_tips, size_height_tips = size_width_main * 32 / 84, size_height_main * 20 / 64
        for i in range(0, 3):
            self.window.blit(pygame.transform.scale(self.fills_tips[i], (int(size_width_tips), int(size_height_tips))),
                             (int(size_width_main + size_width_tubes), int(
                                 starty + self.wheight * 0.01 + size_height_main / 32 + size_height_main * 20 / 64 * i)))

        # Numbers Percents
        size_width_number, size_height_number = size_width_main * 11 / 84, size_height_main * 11 / 64
        for i in range(0, 3):
            self.print_numbers(percentages[i] * 100, True, size_width_number, size_height_number,
                               size_width_main + size_width_tubes,
                               starty + self.wheight * 0.01 + size_height_main / 16 + (
                                       5 * size_height_main / 16) * i + size_height_main / 32)
        # Numbers Plain
        for i in range(0, 3):
            self.print_numbers(plain_numbers[i], False, size_width_number, size_height_number, size_width_main,
                               starty + self.wheight * 0.01 + size_height_main / 16 + (
                                       5 * size_height_main / 16) * i + size_height_main / 32)
