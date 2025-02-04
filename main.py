import pygame
from pygame import *

from DeathScreen import death_screen
from mainclasses import *
from menu import *
import Heal
from Heal import Items
from GUI import GUI
from Enemy import Enemy
from InfiniteScrolling import Scroller
import random
import DeathScreen

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.SCALED, vsync=1)
pygame.display.set_caption("The Souls Adventure")

def main():
    # Initialize pygame

    pygame.init()

    # Define constants for the screen width and height
    # Create the screen object
    # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT

    CameraX, CameraY = 0, 0


    running = True

    BackGround1 = Background('Assets/Woods/background/layer1.png', [0,0])
    BackGround2 = Background('Assets/Woods/background/layer2.png', [0,0])
    BackGround3 = Background('Assets/Woods/background/layer3.png', [0,0])

    num_columns = tile_sheet.get_width()
    num_rows = tile_sheet.get_height()

    # Вызов меню перед игрой

     # создаем героя по (x,y) координатам

    left = right = False
    up = False
    z = False

    entities = pygame.sprite.Group() # Все объекты
    platforms = [] # то, во что мы будем врезаться или опираться
    entities.add()

    level = [
           "                                                                                                                                 8                                                                                                                                                                     400000000000000005                                                                                                                                                                                                                                                                                                                     ",
           "                                                                                                                                 8                                                                                                                                                                     (________________)                                                      12222223                                                                                                                                                                                                                                                       ",
           "                                                                                                                                 8                                                                                                                                                   * e  *    ^  ^                                                                            4      5                                                                                                                                                                                                                                                       ",
           "                                                                                                                                 8                                                                                                                                                  <=====>  <=====>                                                   q                       4      5                                                                                                                                                                                                                                                       ",
           "                                                                                                                                 8                                                                                                                                             <>                                                                      a                       q      5                                                                                                                                                                                                                                                       ",
           "                                                                                                                                 8   #       *  e *                                                                                                                                                     ^  ^  ^  ^  ^  ^  ^^     ^^ * e   *            z                       z      5                                                                                                                                                                                                                                                       ",
           "                                                                                                                   <=>           8   67      122223                        q                                                                                                 6                         <=================================>             12222222222222222222222222222225                                                                                                                                                                                                                                                       ",
           "                                              q                                                             ^                    8    8      400005                        a                                                                                           #          ^  ^  ^  ^                                                  <=>      40000000000000000000000000000005                                                                                                                                                                                                                                                       ",
           "                 <==>                         a                                                          <===>                   86   8      400005         ^              a                                         <====>            q                      *e *    122222222222222222222223                                                         40000000000000000000000000000005                                                                                                                                                                                                                                                       ",
           "                                              a                   ^^                            ^^                               v    8      400005        123             z                                    #^                     a                ^^   12223    400000000000000000000005   * e   *                                    *  e*   7  40000000000000000000000000000005                                                                                                                                                                                                                                                       ",
           "             7                                z                 1223                          122223                             q   68      400005        405     ^  ^^   12223                                13                     a       *e *   1223   40005    400000000000000000000005   122222223                   ^  ^  ^  7   12222222223  40000000000000000000000000000005                                                                                                                                                                                                                                                       ",
           "        -    8         e        ^^^    #    123                 4005   *        ^        * #  400005   *     e    *^^^           z    8      400005        405     12223   40005           ^^^^                 45  123                z      12223   4005   40005    400000000000000000000005   400000005      ^^  ^^      12222222223   40000000005  40000000000000000000000000000005                                                                                                                                                                                                                                                       ",
           "122222222223 8 12222222222222222222222223   405    * e   *7     4005  ^^  *   123    *e  ^ 7  400005   1222222222222222222222222223   8      400005        405     40005   40005  12222222222222222222222222223 45  405        ^^^     123    40005   4005   40005    400000000000000000000005   400000005   122222222223   40000000005   40000000005  40000000000000000000000000000005                                                                                                                                                                                                                                                       ",
           "400000000005 8 40000000000000000000000005   405    12222223     4005  12223   405    1222223  400005   4000000000000000000000000005   8      400005        405     40005   40005  40000000000000000000000000005 45  405       12223    405    40005   4005   40005    400000000000000000000005   400000005   400000000005   40000000005   40000000005  40000000000000000000000000000005                                                                                                                                                                                                                                                       "]

    timer = pygame.time.Clock()
    enemies = []
    x=y=0 # координатыz
    for row in level: # вся строка
        for col in row: # каждый символ
            if col != " ":
                pf = Platform(x, y, col)
                entities.add(pf)
                platforms.append(pf)
                if col == "-":
                    hero = Player(x, y, "Warrior", pf)
                elif col == "e":
                    enemies.append(Enemy(x,y, "Skeleton", pf))
                #создаем блок, заливаем его цветом и рисеум его

            x += PLATFORM_WIDTH #блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT    #то же самое и с высотой
        x = 0

    total_level_width  = len(level[0])*PLATFORM_WIDTH # Высчитываем фактическую ширину уровня
    total_level_height = len(level)*PLATFORM_HEIGHT

    BackGround1 = Scroller(BackGround1, hero)
    BackGround2 = Scroller(BackGround2, hero)
    BackGround3 = Scroller(BackGround3, hero)

    camera = Camera(camera_configure, total_level_width, total_level_height)

    healthbar = GUI(hero, camera)

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
            if event.type == KEYDOWN and event.key == K_f:
                z = True


            if event.type == KEYUP and event.key == K_UP:
                up = False
            if event.type == KEYUP and event.key == K_RIGHT:
                right = False
            if event.type == KEYUP and event.key == K_LEFT:
                left = False
            if event.type == KEYUP and event.key == K_f:
                z = False

        screen.fill([255, 255, 255])

        BackGround1.update()
        BackGround2.update()
        BackGround3.update()

        for bg in ["Left", "Center", "Right"]:
            camera.apply(BackGround1.backs[bg], 6)
            screen.blit(BackGround1.backs["Image"], BackGround1.backs[bg].rect)

        for bg in ["Left", "Center", "Right"]:
            camera.apply(BackGround2.backs[bg], 3)
            screen.blit(BackGround2.backs["Image"], BackGround2.backs[bg].rect)

        for bg in ["Left", "Center", "Right"]:
            camera.apply(BackGround3.backs[bg], 1.5)
            screen.blit(BackGround3.backs["Image"], BackGround3.backs[bg].rect)

        camera.apply(hero)
        camera.update(hero)

        healthbar.update()

        if hero.health <= 0:
            for e in Items:
                e.used = True
            return screen

        for e in enemies:
            camera.apply(e)
            e.update(platforms)
            e.draw(screen)

        hero.update(left, right, up, platforms, z, enemies)

        camera.apply(healthbar, 10000)

        for e in Items:
            if not e.used:
                e.update()
                e.draw(screen)

        if hero.isVisible:
            hero.draw(screen)
        #draw.rect(screen, (255,0,0), hero.attack.rect, 3)

        for e in entities:
            camera.apply(e)
            if e.isVisible:
                screen.blit(e.image, e.rect)

        screen.blit(healthbar.image, healthbar.rect)

        pygame.display.flip()

    pygame.quit()

main_menu(screen)

while True:
    screen = main()
    death_screen(screen)