from pygame import *
from spritehandler import *
import os

MOVE_SPEED = 7
WIDTH = 52
HEIGHT = 110
COLOR = "#008000"
JUMP_POWER = 10
GRAVITY = 0.35  # Сила, которая будет тянуть нас вниз
ANIMATION_DELAY = 0.1  # скорость смены кадров
ICON_DIR = os.path.dirname(__file__)  # Полный путь к каталогу с файлами

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

PLATFORM_WIDTH = 52
PLATFORM_HEIGHT = PLATFORM_WIDTH
PLATFORM_COLOR = "#008000"


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + SCREEN_WIDTH / 2, -t + SCREEN_HEIGHT / 2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - SCREEN_WIDTH), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - SCREEN_HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0  # скорость перемещения. 0 - стоять на месте
        self.startX = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.yvel = 0  # скорость вертикального перемещения
        self.onGround = False  # На земле ли я?
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(Color(COLOR))
        self.image = transform.scale(get_sprite(sheets["Warrior"], warrior[0][0], warrior[0][1], sprite_params["Warrior"][0], sprite_params["Warrior"][1]),(150, 110))
        self.rect = Rect(x, y, WIDTH, HEIGHT) # прямоугольный объект
        self.rect.bottomleft = (x, y)
        self.image.set_colorkey((0, 0, 0))

    def update(self, left, right, up, platforms):

        if up:
            if self.onGround:  # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -JUMP_POWER
            # self.image.fill(Color(COLOR))

        if left:
            self.xvel = -MOVE_SPEED  # Лево = x- n
            self.image = transform.scale(get_sprite(sheets["Warrior"], warrior[0][0], warrior[0][1], sprite_params["Warrior"][0], sprite_params["Warrior"][1], True), (150, 110))
            self.image.set_colorkey((0, 0, 0))
            # self.image.fill(Color(COLOR))

        if right:
            self.xvel = MOVE_SPEED  # Право = x + n
            self.image = transform.scale(get_sprite(sheets["Warrior"], warrior[0][0], warrior[0][1], sprite_params["Warrior"][0], sprite_params["Warrior"][1]), (150, 110))
            self.image.set_colorkey((0, 0, 0))
            # self.image.fill(Color(COLOR))

        if not (left or right):  # стоим, когда нет указаний идти
            self.xvel = 0
            if not up:
                ""  # self.image.fill(Color(COLOR))

        if not self.onGround:
            self.yvel += GRAVITY

        self.onGround = False;  # Мы не знаем, когда мы на земле((
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel  # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком

                if xvel > 0:  # если движется вправо
                    self.rect.right = p.rect.left  # то не движется вправо

                if xvel < 0:  # если движется влево
                    self.rect.left = p.rect.right  # то не движется влево

                if yvel > 0:  # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.onGround = True  # и становится на что-то твердое
                    self.yvel = 0  # и энергия падения пропадает

                if yvel < 0:  # если движется вверх
                    self.rect.top = p.rect.bottom  # то не движется вверх
                    self.yvel = 0  # и энергия прыжка пропадает


class Background(sprite.Sprite):
    def __init__(self, image_file, location):
        sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = transform.scale(image.load(image_file), (SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Platform(sprite.Sprite):
    def __init__(self, x, y, tile):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = transform.scale(get_sprite(tile_sheet, tiles[int(tile)][0], tiles[int(tile)][1], sprite_params["Tile"][0], sprite_params["Tile"][1]), (PLATFORM_WIDTH, PLATFORM_HEIGHT))
        
        self.image.set_colorkey((0, 0, 0))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)