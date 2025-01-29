import pygame

tiles = [
    [1,1],
    [0,0],
    [1,0],
    [3,0],
    [0,2],
    [3,2]
]

def get_sprite(sprite_sheet, x, y, sprite_width, sprite_height):
    sprite_rect = pygame.Rect(x * sprite_width, y * sprite_height, sprite_width, sprite_height)
    sprite_image = pygame.Surface(sprite_rect.size)
    sprite_image.blit(sprite_sheet, (0, 0), sprite_rect)
    return sprite_image        