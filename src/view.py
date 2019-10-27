import pygame
from pygame.locals import *


def load_tile_table(filename, nbx: int, nby: int):
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

    def __init__(self) -> None:
        # Creation de la fenetre
        self.window = pygame.display.set_mode((800, 450), RESIZABLE)
        self.wwidth, self.wheight = pygame.display.get_surface().get_size()

        self.load_assets()

    def load_assets(self):
        # Assets
        self.wall_tiles = load_tile_table("tiles/dungeon_wall.png", 4, 4)
        self.door_tiles = load_tile_table("tiles/dungeon_door.png", 4, 4)
        self.ceiling_tiles = load_tile_table("tiles/dungeon_ceiling.png", 4, 2)
        self.cases_hud = load_tile_table("hud/cases.png", 1, 4)

    def print_room(self, room, char):
        doors = room.doors
        orientation = char.get_orientation()

        tempx, tempy = self.wall_tiles[0].get_size()  # Portes et murs ont la meme taille niveau sprite
        size_width, size_height = int(self.wwidth * 0.55), int(self.wwidth * 0.55 * tempy / tempx)

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
        self.window.blit(pygame.transform.scale(self.ceiling_tiles[7], (size_width, size_height)), (0, 0))

    def print_map(map):
        p = 1

    def resize_event(self, event):
        width, height = event.size
        if width / height != 16 / 9:
            height = (width * 9) // 16
        self.window = pygame.display.set_mode((width, height), RESIZABLE)
        self.wwidth, self.wheight = pygame.display.get_surface().get_size()

    def print_cases_hud(self, cursor):
        tempx, tempy = self.cases_hud[0].get_size()
        size_width, size_height = int(self.wwidth * 0.25), int(self.wwidth * 0.25 * tempy / tempx)

        texts = ["Inventory", "Save", "Quit"]

        if cursor == 0:
            self.window.blit(pygame.transform.scale(self.cases_hud[3], (size_width, size_height)),
                             (int(self.wwidth * 0.56), int(self.wheight * 0.30)))
        else:
            self.window.blit(pygame.transform.scale(self.cases_hud[2], (size_width, size_height)),
                             (int(self.wwidth * 0.56), int(self.wheight * 0.30)))

        for i in range(0, len(texts)):
            if cursor == i + 1:
                self.window.blit(pygame.transform.scale(self.cases_hud[1], (size_width, size_height)),
                                 (int(self.wwidth * 0.56), int(self.wheight * 0.30 + self.wheight * 0.10 * (i + 1))))
            else:
                self.window.blit(pygame.transform.scale(self.cases_hud[0], (size_width, size_height)),
                                 (int(self.wwidth * 0.56), int(self.wheight * 0.30 + self.wheight * 0.10 * (i + 1))))
