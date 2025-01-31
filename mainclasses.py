import pygame
from pygame import *
from spritehandler import *
from animator import Animation
import os

TYPICAL_ANIMS = {
    "Warrior": {
        "Idle": (1,0),
        "Walk": (1,0),
        "Jump": (0,1),
        #"Attack": (0,0)
    }
}

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
    def __init__(self, x, y, charType):
        sprite.Sprite.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.Animations = {
            "Left": {},
            "Right": {}
        }
        self.facing = "Right"
        self.charType = charType

        # Загружаем спрайт
        self.sprite_width = 150
        self.sprite_height = 110
        self.image = transform.scale(
            get_sprite(sheets["Warrior"], warrior[0][0], warrior[0][1], sprite_params["Warrior"][0], sprite_params["Warrior"][1]),
            (self.sprite_width, self.sprite_height)
        )
        self.image.set_colorkey((0, 0, 0))

        # Создаем хитбокс (уменьшим его, чтобы он совпадал с ногами персонажа)
        self.hitbox_width = 50
        self.hitbox_height = 90  # Подкорректируйте, если нужно
        self.rect = Rect(x, y, self.hitbox_width, self.hitbox_height)

        for direction in ["Left", "Right"]:
            for anim, params in TYPICAL_ANIMS[self.charType].items():
                self.Animations[direction][anim] = Animation(anim, self.charType, direction, params[0], params[1])

    def update(self, left, right, up, platforms):
        if up and self.onGround:
            self.yvel = -JUMP_POWER

        if left:
            self.xvel = -MOVE_SPEED
            self.image = transform.scale(
                get_sprite(sheets["Warrior"], warrior[0][0], warrior[0][1], sprite_params["Warrior"][0], sprite_params["Warrior"][1], True),
                (self.sprite_width, self.sprite_height)
            )
            self.facing = "Left"
            self.image.set_colorkey((0, 0, 0))

        if right:
            self.xvel = MOVE_SPEED
            self.image = transform.scale(
                get_sprite(sheets["Warrior"], warrior[0][0], warrior[0][1], sprite_params["Warrior"][0], sprite_params["Warrior"][1], False),
                (self.sprite_width, self.sprite_height)
            )
            self.facing = "Right"
            self.image.set_colorkey((0, 0, 0))

        if not (left or right):
            self.xvel = 0

        if not self.onGround:
            self.yvel += GRAVITY

        self.onGround = False
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0

    def draw(self, screen):
        # Рисуем хитбокс (для отладки)
        pygame.draw.rect(screen, (0, 255, 0), self.rect, 2)  # Зеленый контур хитбокса

        # Смещаем спрайт так, чтобы он находился над хитбоксом
        sprite_x = self.rect.x - (self.sprite_width - self.hitbox_width) // 2
        sprite_y = self.rect.y - (self.sprite_height - self.hitbox_height)

        # Рисуем спрайт поверх хитбокса
        screen.blit(self.image, (sprite_x, sprite_y))


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
        self.image = transform.scale(get_sprite(tile_sheet, tiles[int(tile)][0], tiles[int(tile)][1], sprite_params["Tile"][0], sprite_params["Tile"][1]),
                                     (PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.set_colorkey((0, 0, 0))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)