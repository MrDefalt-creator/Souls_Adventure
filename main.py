# Import the pygame module
import pygame
from pygame import *
from mainclasses import *
from menu import *
from InfiniteScrolling import Scroller
import random

# Initialize pygame
pygame.init()

# Define constants for the screen width and height
# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.SCALED, vsync=1)
pygame.display.set_caption("The Epic Adventure")

CameraX, CameraY = 0, 0


running = True

BackGround1 = Background('Assets/Woods/background/layer1.png', [0,0])
BackGround2 = Background('Assets/Woods/background/layer2.png', [0,0])
BackGround3 = Background('Assets/Woods/background/layer3.png', [0,0])

num_columns = tile_sheet.get_width()
num_rows = tile_sheet.get_height()

# Вызов меню перед игрой
main_menu(screen)

hero = Player(200,600, "Warrior") # создаем героя по (x,y) координатам

BackGround1 = Scroller(BackGround1, hero)
BackGround2 = Scroller(BackGround2, hero)
BackGround3 = Scroller(BackGround3, hero)

left = right = False
up = False
z = False

entities = pygame.sprite.Group() # Все объекты
platforms = [] # то, во что мы будем врезаться или опираться
entities.add()

level = [
       "                                                                                                              ",
       "                                                                                                              ",
       "                                                                                                              ",
       "                                                                                                              ",
       "                             6                                                                                ",
       "                                                                                                              ",
       "                        6                                                                                     ",
       "                                                                                                              ",
       "                 6                                                                                            ",
       "                                                                                                              ",
       "           7                                                                                                  ",
       "           8                                                                                                  ",
       "12222222222222222222222222222222222222223     1222222222222222222222222222222222222222222222222222222222222223",
       "40000000000000000000000000000000000000005     4000000000000000000000000000000000000000000000000000000000000005"]

timer = pygame.time.Clock()
x=y=0 # координатыz
for row in level: # вся строка
    for col in row: # каждый символ
        if col != " ":
            #создаем блок, заливаем его цветом и рисеум его
            pf = Platform(x,y,col)
            entities.add(pf)
            platforms.append(pf)
                    
        x += PLATFORM_WIDTH #блоки платформы ставятся на ширине блоков
    y += PLATFORM_HEIGHT    #то же самое и с высотой
    x = 0         

total_level_width  = len(level[0])*PLATFORM_WIDTH # Высчитываем фактическую ширину уровня
total_level_height = len(level)*PLATFORM_HEIGHT

camera = Camera(camera_configure, total_level_width, total_level_height)

# Main loop

while running:
    timer.tick(60)
    # Look at every event in the queue
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == KEYDOWN and event.key == K_UP:
            up = True
        if event.type == KEYDOWN and event.key == K_LEFT:
            left = True
        if event.type == KEYDOWN and event.key == K_RIGHT:
            right = True
        if event.type == KEYDOWN and event.key == K_z:
            z = True


        if event.type == KEYUP and event.key == K_UP:
            up = False
        if event.type == KEYUP and event.key == K_RIGHT:
            right = False
        if event.type == KEYUP and event.key == K_LEFT:
            left = False
        if event.type == KEYUP and event.key == K_z:
            z = False
    
    screen.fill([255, 255, 255])

    for bg in ["Left", "Center", "Right"]:
        camera.apply(BackGround1.backs[bg], 6)
        screen.blit(BackGround1.backs["Image"], BackGround1.backs[bg].rect)

    for bg in ["Left", "Center", "Right"]:
        camera.apply(BackGround2.backs[bg], 3)
        screen.blit(BackGround2.backs["Image"], BackGround2.backs[bg].rect)

    for bg in ["Left", "Center", "Right"]:
        camera.apply(BackGround3.backs[bg], 1.5)
        screen.blit(BackGround3.backs["Image"], BackGround3.backs[bg].rect)

    for e in entities:
        camera.apply(e)
        screen.blit(e.image, e.rect)

    camera.apply(hero)
    camera.update(hero)
    hero.update(left, right, up, platforms, z) # передвижение

    hero.draw(screen)

    BackGround1.update()
    BackGround2.update()
    BackGround3.update()

    pygame.display.update()

pygame.quit()