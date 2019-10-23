import pygame
from pygame.locals import *

# Initialisation de la bibliotheque Pygame
pygame.init()

# Creation de la fenetre
window = pygame.display.set_mode((640, 480), RESIZABLE)

wall_tiles = pygame.image.load("tiles/dungeon_wall.png").convert_alpha()
door_tiles = pygame.image.load("tiles/dungeon_door.png").convert_alpha()
ceiling_tiles = pygame.image.load("tiles/dungeon_ceiling.png").convert_alpha()


def print_tile(posx, scale, tiles):
    w, h = tiles.get_size()
    tile_rect = pygame.Rect((160 * posx * scale) % (w * scale), (posx // 4) * 120 * scale, 160 * scale, 120 * scale)
    resized = pygame.transform.scale(tiles, (w * scale, h * scale))
    window.blit(resized, (0, 0), tile_rect)

def print_room(room, char):


print_tile(6, 4, wall_tiles)
print_tile(7, 4, wall_tiles)
print_tile(5, 4, door_tiles)
print_tile(7, 4, ceiling_tiles)

pygame.display.flip()

# Boucle infinie
close = False
while not close:
    for event in pygame.event.get():
        if event.type == QUIT:
            close = True
