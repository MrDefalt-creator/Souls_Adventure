# Import the pygame module
import pygame
from pygame import *
from mainclasses import *
from menu import *
import random

# Initialize pygame
pygame.init()


def generate_level(width, height):
    level = []
    for _ in range(height):
        level.append([' '] * width)  # Пустые места пробелами

    # Создаем землю внизу (платформа с краями)
    if width >= 2:
        ground_row = ['4'] + ['2'] * (width - 2) + ['5']
    else:
        ground_row = ['4'] * width
    level[-1] = ground_row

    current_x = 5
    current_y = height - 5  # Начальная позиция над землей

    # Генерация основных платформ
    while current_x < width - 5:
        platform_length = random.randint(2, 5)
        end_x = current_x + platform_length
        if end_x >= width:
            end_x = width - 1
            platform_length = end_x - current_x

        # Левый край платформы
        if current_x < width:
            level[current_y][current_x] = '4'
        # Середина
        for x in range(current_x + 1, end_x):
            if x < width:
                level[current_y][x] = '2'
        # Правый край
        if end_x < width:
            level[current_y][end_x] = '5'

        # Переход к следующей платформе
        current_x += platform_length + random.randint(2, 4)
        # Изменение высоты
        delta_y = random.randint(-2, 2)
        current_y = max(3, min(current_y + delta_y, height - 2))

    # Добавляем случайные небольшие платформы
    for _ in range(20):
        plat_x = random.randint(0, width - 3)
        plat_y = random.randint(3, height - 4)
        if (plat_x + 2 < width and
                level[plat_y][plat_x] == ' ' and
                level[plat_y][plat_x + 1] == ' ' and
                level[plat_y][plat_x + 2] == ' '):
            level[plat_y][plat_x] = '4'
            level[plat_y][plat_x + 1] = '2'
            level[plat_y][plat_x + 2] = '5'

    return [''.join(row) for row in level]
# Define constants for the screen width and height
# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Epic Adventure")

running = True

BackGround1 = Background('Assets/Woods/background/layer1.png', [0,0])
BackGround2 = Background('Assets/Woods/background/layer2.png', [0,0])
BackGround3 = Background('Assets/Woods/background/layer3.png', [0,0])

num_columns = tile_sheet.get_width()
num_rows = tile_sheet.get_height()

# Вызов меню перед игрой
main_menu(screen)

hero = Player(200,600, "Warrior") # создаем героя по (x,y) координатам
left = right = False
up = False
z = False
z = False

entities = pygame.sprite.Group() # Все объекты
platforms = [] # то, во что мы будем врезаться или опираться
entities.add()

level = [
       "4",
       "4",
       "4",
       "4",
       "4",
       "4",
       "4",
       "4",
       "4                6",
       "4",
       "4          7",
       "4          8",
       "4222222222222222222222223",
       "4000000000000000000000005"]

timer = pygame.time.Clock()
x=y=0 # координатыz
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
        if event.type == KEYUP and event.key == K_z:
            z = False
    
    screen.fill([255, 255, 255])
    screen.blit(BackGround1.image, BackGround1.rect)
    screen.blit(BackGround2.image, BackGround2.rect)
    screen.blit(BackGround3.image, BackGround3.rect)

    for e in entities:
        screen.blit(e.image, e.rect)

    #camera.update(hero)
    hero.update(left, right, up, platforms, z) # передвижение
    hero.update(left, right, up, platforms, z) # передвижение
    hero.draw(screen)
    pygame.display.update() 

pygame.quit()