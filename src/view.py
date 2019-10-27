import pygame
from pygame.locals import *


def load_tile_table(filename, width: int, height: int):
    image = pygame.image.load(filename).convert_alpha()
    image_width, image_height = image.get_size()
    tile_table = []

    for tile_y in range(0, image_height // height):
        for tile_x in range(0, image_width // width):
            rect = (tile_x * width, tile_y * height, width, height)
            tile_table.append(image.subsurface(rect))
    return tile_table


class View:
    window = None
    wwidth, wheight = 0, 0
    # Assets
    wall_tiles = None
    door_tiles = None
    ceiling_tiles = None

    def __init__(self) -> None:
        # Creation de la fenetre
        self.window = pygame.display.set_mode((800, 450), RESIZABLE)
        self.wwidth, self.wheight = pygame.display.get_surface().get_size()

        self.load_assets()

    def load_assets(self):
        # Assets
        self.wall_tiles = load_tile_table("tiles/dungeon_wall.png", 640 // 4, 480 // 4)
        self.door_tiles = load_tile_table("tiles/dungeon_door.png", 640 // 4, 480 // 4)
        self.ceiling_tiles = load_tile_table("tiles/dungeon_ceiling.png", 640 // 4, 480 // 4)

    def print_room(self, room, char):
        doors = room.doors
        orientation = char.get_orientation()

        for i in range(0, orientation):
            doors.append(doors.pop(0))

        tempx, tempy = self.wall_tiles[0].get_size()  # Portes et murs ont la meme taille niveau sprite
        size_width, size_height = int(self.wwidth * 0.55), int(self.wwidth * 0.55 * tempy / tempx)

        if doors[0]:
            self.window.blit(pygame.transform.scale(self.door_tiles[5], (size_width, size_height)), (0, 0))
        else:
            self.window.blit(pygame.transform.scale(self.wall_tiles[5], (size_width, size_height)), (0, 0))
        if doors[-1]:
            self.window.blit(pygame.transform.scale(self.door_tiles[7], (size_width, size_height)), (0, 0))
        else:
            self.window.blit(pygame.transform.scale(self.wall_tiles[7], (size_width, size_height)), (0, 0))
        if doors[1]:
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
