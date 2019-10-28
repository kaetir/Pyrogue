import pygame
from pygame.locals import *


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
        self.wall_tiles = load_tile_table("tiles/dungeon_wall.png", 4, 4)
        self.door_tiles = load_tile_table("tiles/dungeon_door.png", 4, 4)
        self.ceiling_tiles = load_tile_table("tiles/dungeon_ceiling.png", 4, 4)
        self.cases_hud = load_tile_table("hud/cases.png", 1, 12)
        self.fills_fillers = load_tile_table("hud/fills_fillers.png", 1, 3)
        self.fills_tips = load_tile_table("hud/fills_tips.png", 1, 3)
        self.fills_main = load_tile_table("hud/fills_main.png", 4, 1)
        self.fills_tubes = load_tile_table("hud/fills_tubes.png", 1, 1)
        self.numbers_tiles = load_tile_table("hud/numbers.png", 11, 1)

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

    def print_map(self):
        """
        @brief Affichage de la map a l'ecran
        """
        map = load_tile_table("map.png", 1, 1)
        tempx, tempy = map[0].get_size()
        size_width, size_height = int(self.wheight * 0.30 * tempx / tempy), int(self.wheight * 0.30)
        self.window.blit(pygame.transform.scale(map[0], (size_width, size_height)),
                         (int(self.wwidth * (0.55 + 0.45 / 2) - size_width / 2), 0))

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
        size_width, size_height = int(self.wwidth * 0.25), int(self.wwidth * 0.25 * tempy / tempx)

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
                                 (int(self.wwidth * 0.56), int(self.wheight * 0.30 + self.wheight * 0.10 * (i + 1))))
            else:
                self.window.blit(pygame.transform.scale(self.cases_hud[i * 2 + 2], (size_width, size_height)),
                                 (int(self.wwidth * 0.56), int(self.wheight * 0.30 + self.wheight * 0.10 * (i + 1))))

        if exit_case or merchant_case:
            i = 0
            if exit_case:
                i = 0
            elif merchant_case:
                i = i
            if cursor == 3:
                self.window.blit(pygame.transform.scale(self.cases_hud[i * 2 + 7], (size_width, size_height)),
                                 (int(self.wwidth * 0.56), int(self.wheight * 0.30 + self.wheight * 0.10 * 3)))
            else:
                self.window.blit(pygame.transform.scale(self.cases_hud[i * 2 + 6], (size_width, size_height)),
                                 (int(self.wwidth * 0.56), int(self.wheight * 0.30 + self.wheight * 0.10 * 3)))



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
        percentages = [char.get_life_percent(), char.get_mana_percent(), char.get_armor_percent()]
        plain_numbers = [char.get_health(), char.get_mana(), char.get_armor()]

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
