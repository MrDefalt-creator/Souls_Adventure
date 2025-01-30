# Import the pygame module
import pygame
from pygame import *
from mainclasses import *
from menu import *

# Initialize pygame
pygame.init()

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

hero = Player(55,600) # создаем героя по (x,y) координатам
left = right = False
up = False

entities = pygame.sprite.Group() # Все объекты
platforms = [] # то, во что мы будем врезаться или опираться

level = [
       "5",
       "5",
       "5",
       "5",
       "5",
       "5",
       "5",
       "5",
       "5",
       "5",
       "5",
       "5         2",
       "5222222222222222222222223",
       "5000000000000000000000005"]

timer = pygame.time.Clock()
x=y=0 # координаты
for row in level: # вся строка
    for col in row: # каждый символ
        if col != " ":
            #создаем блок, заливаем его цветом и рисуем его
            pf = Platform(x,y,col)
            entities.add(pf)
            platforms.append(pf)
                    
        x += PLATFORM_WIDTH #блоки платформы ставятся на ширине блоков
    y += PLATFORM_HEIGHT    #то же самое и с высотой
    x = 0         

total_level_width  = len(level[0])*PLATFORM_WIDTH # Высчитываем фактическую ширину уровня
total_level_height = len(level)*PLATFORM_HEIGHT

camera = Camera(camera_configure, total_level_width, total_level_height) 

# Вызов меню перед игрой
main_menu(screen)


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


        if event.type == KEYUP and event.key == K_UP:
            up = False
        if event.type == KEYUP and event.key == K_RIGHT:
            right = False
        if event.type == KEYUP and event.key == K_LEFT:
            left = False
    
    screen.fill([255, 255, 255])
    screen.blit(BackGround1.image, BackGround1.rect)
    screen.blit(BackGround2.image, BackGround2.rect)
    screen.blit(BackGround3.image, BackGround3.rect)

    for e in entities:
        screen.blit(e.image, e.rect)
        draw.rect(screen, (0,0,0), e.rect)

    #camera.update(hero)
    hero.update(left, right, up, platforms) # передвижение
    screen.blit(hero.image, hero.rect)
    pygame.draw.rect(screen, (0,0,0), hero.rect)
    pygame.display.update() 

pygame.quit()