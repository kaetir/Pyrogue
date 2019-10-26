import pygame
from pygame.locals import *


class View:
    def load_tile_table(filename, width: int, height: int):
        image = pygame.image.load(filename).convert_alpha()
        image_width, image_height = image.get_size()
        tile_table = []

        for tile_y in range(0, image_height // height):
            for tile_x in range(0, image_width // width):
                rect = (tile_x * width, tile_y * height, width, height)
                tile_table.append(image.subsurface(rect))
        return tile_table

    # Assets
    wall_tiles = load_tile_table("tiles/dungeon_wall.png", 640 // 4, 480 // 4)
    door_tiles = load_tile_table("tiles/dungeon_door.png", 640 // 4, 480 // 4)
    ceiling_tiles = load_tile_table("tiles/dungeon_ceiling.png", 640 // 4, 480 // 4)

    # Initialisation de la bibliotheque Pygame
    pygame.init()
    # Creation de la fenetre
    window = pygame.display.set_mode((800, 450), RESIZABLE)
    wwidth, wheight = pygame.display.get_surface().get_size()

    def print_room(self,room, char):
        doors = room  # .door
        orientation = char  # .orientation

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

    def start_game(self):
        clock = pygame.time.Clock()

        # Boucle infinie
        close = False
        i = 1
        while not close:
            # Treating Events
            for event in pygame.event.get():
                if event.type == QUIT:
                    close = True
                elif event.type == VIDEORESIZE:
                    wwidth, wheight = event.size
                    if wwidth / wheight != 16 / 9:
                        wheight = (wwidth * 9) // 16
                    window = pygame.display.set_mode((wwidth, wheight), RESIZABLE)

            wwidth, wheight = pygame.display.get_surface().get_size()
            i += 1
            # Calculating New sprites and Printing
            self.print_room([0, 1, 1, 0], i // 30)
            pygame.display.flip()

            # Ticking
            clock.tick(30)
