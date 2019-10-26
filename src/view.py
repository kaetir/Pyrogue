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


def print_room(room, char):
    doors = room#.door
    orientation = char#.orientation

    for i in range(0, orientation):
        doors.append(doors.pop(0))

    tempx, tempy = wall_tiles[0].get_size() # Portes et murs ont la meme taille niveau sprite

    if doors[0]:
        window.blit(pygame.transform.scale(door_tiles[5], (int(wwidth * 0.55), int(wwidth * 0.55 * tempy / tempx))),(0, 0))
    else:
        window.blit(pygame.transform.scale(wall_tiles[5], (int(wwidth * 0.55), int(wwidth * 0.55 * tempy / tempx))),(0, 0))
    if doors[-1]:
        window.blit(pygame.transform.scale(door_tiles[7], (int(wwidth * 0.55), int(wwidth * 0.55 * tempy / tempx))),(0, 0))
    else:
        window.blit(pygame.transform.scale(wall_tiles[7], (int(wwidth * 0.55), int(wwidth * 0.55 * tempy / tempx))),(0, 0))
    if doors[1]:
        window.blit(pygame.transform.scale(door_tiles[6], (int(wwidth * 0.55), int(wwidth * 0.55 * tempy / tempx))),(0, 0))
    else:
        window.blit(pygame.transform.scale(wall_tiles[6], (int(wwidth * 0.55), int(wwidth * 0.55 * tempy / tempx))),(0, 0))
    window.blit(pygame.transform.scale(ceiling_tiles[7], (int(wwidth * 0.55), int(wwidth * 0.55 * tempy / tempx))),(0, 0))


def print_map(map):
    p=1

# Initialisation de la bibliotheque Pygame
pygame.init()

# Creation de la fenetre
window = pygame.display.set_mode((800, 450), RESIZABLE)

wall_tiles = load_tile_table("tiles/dungeon_wall.png", 640 // 4, 480 // 4)
door_tiles = load_tile_table("tiles/dungeon_door.png", 640 // 4, 480 // 4)
ceiling_tiles = load_tile_table("tiles/dungeon_ceiling.png", 640 // 4, 480 // 4)

# resized = pygame.transform.scale(tiles, (w * scale, h * scale))
window.blit(wall_tiles[6], (0, 0))

clock = pygame.time.Clock()

# Boucle infinie
close = False
i=1
while not close:
    # Treating Events
    for event in pygame.event.get():
        if event.type == QUIT:
            close = True
        elif event.type == VIDEORESIZE:
            wwidth, wheight = event.size
            if wwidth/wheight != 16/9:
                wheight = (wwidth * 9) // 16
            window = pygame.display.set_mode((wwidth, wheight), RESIZABLE)

    wwidth, wheight = pygame.display.get_surface().get_size()
    i+=1
    # Calculating New sprites and Printing
    print_room([0,1,1,0],i//30)
    pygame.display.flip()

    # Ticking
    clock.tick(30)
