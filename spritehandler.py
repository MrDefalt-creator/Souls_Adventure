from pygame import *

tile_sheet = image.load("Assets/Woods/oak_woods_tileset.png")
warrior_sheet = image.load("Assets/Warrior/adventurer-sheet2.png")

w_width = 50
w_height = 37

tiles = [
    [1,1],
    [0,0],
    [1,0],
    [3,0],
    [0,2],
    [3,2]
]

warrior = [
    [0,0]
]

def get_sprite(sprite_sheet, x, y, sprite_width, sprite_height, flipped = False):
    sprite_rect = Rect(x * sprite_width, y * sprite_height, sprite_width, sprite_height)
    sprite_image = Surface(sprite_rect.size)
    sprite_image.blit(sprite_sheet, (0, 0), sprite_rect)
    return transform.flip(sprite_image, True, False) if flipped else sprite_image        