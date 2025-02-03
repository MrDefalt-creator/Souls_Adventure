import pygame
import sys
from mainclasses import *
# Константы
BG_COLOR = (30, 30, 30)
WHITE = (255, 255, 255)  # Возвращаем белый цвет для текста
HIGHLIGHT = (200, 200, 200)
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
# Инициализация Pygame
pygame.init()

# Шрифт
font = pygame.font.Font("./Assets/Font/Silver.ttf", 100)

# Функция отрисовки текста
def draw_text(text, x, y, color, screen):
    render = font.render(text, True, color)
    rect = render.get_rect(center=(x, y))
    screen.blit(render, rect)
    return rect

# Функция главного меню
def death_screen(screen, hero):
    # Загрузка статичных слоев фона
    bg1 = pygame.image.load('Assets/Woods/background/layer1.png').convert_alpha()
    bg2 = pygame.image.load('Assets/Woods/background/layer2.png').convert_alpha()
    bg3 = pygame.image.load('Assets/Woods/background/layer3.png').convert_alpha()

    # Растягиваем фоны на весь экран
    bg1 = pygame.transform.scale(bg1, (SCREEN_WIDTH, SCREEN_HEIGHT))
    bg2 = pygame.transform.scale(bg2, (SCREEN_WIDTH, SCREEN_HEIGHT))
    bg3 = pygame.transform.scale(bg3, (SCREEN_WIDTH, SCREEN_HEIGHT))

    while True:
        screen.fill(BG_COLOR)

        mx, my = pygame.mouse.get_pos()

        # Отрисовка статичных фоновых слоев, растянутых на весь экран
        screen.blit(bg1, (0, 0))  # Первый слой фона
        screen.blit(bg2, (0, 0))  # Второй слой фона
        screen.blit(bg3, (0, 0))  # Третий слой фона

# Заголовок чуть выше
        draw_text("Вы погибли", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200, HIGHLIGHT, screen)

        # Кнопка "Попробовать снова" ближе к центру
        retry_button = draw_text(
            "Попробовать снова",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 80,
            WHITE if SCREEN_WIDTH // 3 < mx < SCREEN_WIDTH * 2 / 3 and SCREEN_HEIGHT // 2 - 105 < my < SCREEN_HEIGHT // 2 - 55 else HIGHLIGHT,
            screen
        )

        # Кнопка "Выход" ещё ниже
        exit_button = draw_text(
            "Выход",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 80,
            WHITE if SCREEN_WIDTH // 3 < mx < SCREEN_WIDTH * 2 / 3 and SCREEN_HEIGHT // 2 + 55 < my < SCREEN_HEIGHT // 2 + 105 else HIGHLIGHT,
            screen
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button.collidepoint(mx, my):
                    hero.respawn(True)
                    hero.health = 4
                    return # Запуск игры
                if exit_button.collidepoint(mx, my):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
