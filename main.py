import pygame
from pygame import *

from EndScreen import death_screen, win_screen
from mainclasses import *
from menu import *
from Heal import Items
from GUI import GUI
from Enemy import Enemy
from witch import Witch
from InfiniteScrolling import Scroller

from LevelSelector import level_selector_screen

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.SCALED, vsync=1)
pygame.display.set_caption("The Souls Adventure")

def main():
    # Initialize pygame

    pygame.init()

    # Define constants for the screen width and height
    # Create the screen object
    # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT

    running = True

    BackGround1 = Background('Assets/Woods/background/layer1.png', [0,0])
    BackGround2 = Background('Assets/Woods/background/layer2.png', [0,0])
    BackGround3 = Background('Assets/Woods/background/layer3.png', [0,0])

    num_columns = tile_sheet.get_width()
    num_rows = tile_sheet.get_height()

    # Вызов меню перед игрой

    # создаем героя по (x,y) координатам

    left = right = False
    down = False
    up = False
    antihold = False
    z = False
    c = False

    entities = pygame.sprite.Group() # Все объекты
    platforms = [] # то, во что мы будем врезаться или опираться
    entities.add()
    timer = pygame.time.Clock()

    level = level_selector_screen(screen)

    x=y=0 # координаты
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

    walls = [
        namespace(rect = Rect(0, 0, 20, 720)),
        namespace(rect = Rect(1260, 0, 20, 720))
    ]

    # Main loop
    while running:
        timer.tick(100)
        # Look at every event in the queue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == KEYDOWN and event.key == K_x:
                up = True
            if event.type == KEYDOWN and event.key == K_LEFT:
                left = True
            if event.type == KEYDOWN and event.key == K_RIGHT:
                right = True
            if event.type == KEYDOWN and event.key == K_DOWN:
                down = True
            if event.type == KEYDOWN and event.key == K_z:
                z = True
            if event.type == KEYDOWN and event.key == K_c:
                c = True


            if event.type == KEYUP and event.key == K_x:
                up = False
                antihold = False
            if event.type == KEYUP and event.key == K_RIGHT:
                right = False
            if event.type == KEYUP and event.key == K_LEFT:
                left = False
            if event.type == KEYUP and event.key == K_DOWN:
                down = False
            if event.type == KEYUP and event.key == K_z:
                z = False
            if event.type == KEYUP and event.key == K_c:
                c = False

        screen.fill([255, 255, 255])

        BackGround1.update()
        BackGround2.update()
        BackGround3.update()

        for bg in ["Left", "Center", "Right"]:
            if hero.isFollowed:
                camera.apply(BackGround1.backs[bg], 6)
            screen.blit(BackGround1.backs["Image"], BackGround1.backs[bg].rect)

        for bg in ["Left", "Center", "Right"]:
            if hero.isFollowed:
                camera.apply(BackGround2.backs[bg], 3)
            screen.blit(BackGround2.backs["Image"], BackGround2.backs[bg].rect)

        for bg in ["Left", "Center", "Right"]:
            if hero.isFollowed:    
                camera.apply(BackGround3.backs[bg], 1.5)
            screen.blit(BackGround3.backs["Image"], BackGround3.backs[bg].rect)

        if hero.isFollowed:
            camera.apply(hero)
            camera.update(hero)

        healthbar.update()

        if hero.health <= 0:
            for e in Items:
                e.used = True
            return screen, False

        for e in enemies:
            if hero.isFollowed:
                camera.apply(e)
            e.update(platforms, hero)
            e.draw(screen)

        if antihold:
            up = False
        for a in Attacks:
            if hero.isFollowed:
                camera.apply(a)
            a.update()

        hero.update(left, right, up, down, platforms, z, c, enemies, walls, Attacks)

        if hero.triggerBoss:
            enemies.append(Witch(1100, -150, "Witch"))
            hero.triggerBoss = False

        if up:
            antihold = True

        camera.apply(healthbar, 10000)

        for e in Items:
            if not e.used:
                if hero.isFollowed:
                    e.update()
                e.draw(screen)

        #draw.rect(screen, (0,0,255), hero.rect, 1)
        #draw.rect(screen, (0,0,255), hero.attack.rect, 3)
        if hero.isVisible:
            hero.draw(screen)

        if hero.won:
            return screen, True

        for e in entities:
            if hero.isFollowed:
                camera.apply(e)
            if e.isVisible:
                screen.blit(e.image, e.rect)

        screen.blit(healthbar.image, healthbar.rect)

        display.flip()

    quit()

main_menu(screen)

while True:
    screen, win = main()
    if win:
        win_screen(screen)
    else:
        death_screen(screen)