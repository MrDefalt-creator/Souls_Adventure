from pygame import *

tile_sheet = image.load("Assets/Woods/oak_woods_tileset.png")
sheets = {
    "Warrior": image.load("Assets/Warrior/adventurer-sheet2.png")
}

sprite_params = {
    "Tile": (24,24),
    "Warrior": (50,37),
    "Witch": ()
}

tiles = [
    [1,1],
    [0,0],
    [1,0],
    [3,0],
    [0,2],
    [3,2],
    [10,0],
    [6,2],
    [6,4]
]

warrior = [
    [0,0]
]

def get_sprite(sprite_sheet, x, y, sprite_width, sprite_height, flipped = False):
    sprite_rect = Rect(x * sprite_width, y * sprite_height, sprite_width, sprite_height)
    sprite_image = Surface(sprite_rect.size)
    sprite_image.blit(sprite_sheet, (0, 0), sprite_rect)
    return transform.flip(sprite_image, True, False) if flipped else sprite_image        