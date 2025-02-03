from pygame import *

tile_sheet = image.load("Assets/Woods/oak_woods_tileset.png")
health_sheet = image.load("Assets/UI/LifeSheet.png")
sheets = {
    "Warrior": image.load("Assets/Warrior/adventurer-sheet2.png"),
    "Skeleton": image.load("Assets/Skeleton/sprite-sheet.png")
}

sprite_params = {
    "Tile": (24,24),
    "Warrior": (50,37),
    "Witch": (),
    "Health": (64, 16),
    "Skeleton":(150,150)
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
    "#": [4,0]
}

health = [[0,0],[0,1],[0,2],[0,3],[0,4]]

warrior = [
    [0,0]
]

def get_sprite(sprite_sheet, x, y, sprite_width, sprite_height, flipped = False):
    sprite_rect = Rect(x * sprite_width, y * sprite_height, sprite_width, sprite_height)
    sprite_image = Surface(sprite_rect.size)
    sprite_image.blit(sprite_sheet, (0, 0), sprite_rect)
    return transform.flip(sprite_image, True, False) if flipped else sprite_image        