from pygame import *

tile_sheet = image.load("Assets/Woods/oak_woods_tileset.png")
health_sheet = image.load("Assets/UI/LifeSheet.png")
sheets = {
    "Warrior": image.load("Assets/Warrior/adventurer-sheet2.png"),
    "Skeleton": image.load("Assets/Skeleton/sprite-sheet.png"),
    "Witch": image.load("Assets/Witch/witch-sheet.png"),
    "Ice": image.load("Assets/IceVFX1/ice-sheet.png"),
    "Ice2": image.load("Assets/IceVFX1/ice-sheet2.png")
}

sprite_params = {
    "Tile": (24,24),
    "Warrior": (50,37),
    "Health": (64, 16),
    "Skeleton":(150,150),
    "Witch": (32, 48),
    "Ice": (192, 192),
    "Ice2": (576, 576)
}

tiles = {
    "0": [1,1],
    "1": [0,0],
    "2": [1,0],
    "3": [3,0],
    "4": [0,2],
    "5": [3,2],
    "6": [10,0],
    "7": [6,2],
    "8": [6,4],
    "-": [4,0],
    "e": [4,0],
    "^": [4,3],
    "*": [4,0],
    "#": [4,0],
    "<": [9,3],
    "=": [12,10],
    ">": [11,3],
    "(": [0,3],
    "_": [1,3],
    ")": [3,3],
    "u": [6,5],
    "q": [15,10],
    "a": [15,6],
    "z": [15,11],
    "!": [4,0],
    ";": [4,0],
    ":": [4,0],
    "@": [4,0],
    "?": [4,0]
}

health = [[0,0],[0,1],[0,2],[0,3],[0,4]]

placeholder = [0,0]

def get_sprite(sprite_sheet, x, y, sprite_width, sprite_height, flipped = False, vertical = False):
    sprite_rect = Rect(x * sprite_width, y * sprite_height, sprite_width, sprite_height)
    sprite_image = Surface(sprite_rect.size).convert_alpha()
    sprite_image.blit(sprite_sheet, (0, 0), sprite_rect)
    return transform.flip(sprite_image, flipped, vertical)