import time
import pygame
from pygame import *
from spritehandler import *
from types import SimpleNamespace as namespace
from animator import *
from Heal import Items
import os
import EndScreen

directions = {
    "Right": 1,
    "Left": -1
}

cantCollide = ["-", "e", "^", "*", "#", "!"]

destructable = ["q", "a", "z"]

TYPICAL_ANIMS = {
    "Warrior": {
        "Idle": (1,0,170),
        "Walk": (1,0,100),
        "Jump": (0,0,75),
        "Fall": (1,0,100),
        "Attack1": (0,0,75),
        "Attack2": (0,0,75),
        "Attack3": (0,0,50),
        "WallSlide": (1,0,100),
        "Crouch": (1,0,170),
        "Slide": (0,0,100),
        "Parry": (1,0,100),
        "Counter": (0,0,150)
    },
    "Skeleton":{
        "Idle": (1,0,170),
        "Walk": (1,0,100),
        "Take_hit": (0,0,100),
        "Death": (0,1,100),
        "Attack": (0,0,100)
    }
    
}

MOVE_SPEED = 7
WIDTH = 52
HEIGHT = 110
COLOR = "#008000"
JUMP_POWER = 10
GRAVITY = 0.35  # Сила, которая будет тянуть нас вниз
ACTUAL_GRAVITY = 0.35
ANIMATION_DELAY = 0.1  # скорость смены кадров
ICON_DIR = os.path.dirname(__file__)  # Полный путь к каталогу с файлами

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

PLATFORM_WIDTH = 52
PLATFORM_HEIGHT = PLATFORM_WIDTH
PLATFORM_COLOR = "#008000"

def clamp(n, smallest, largest): return max(smallest, min(n, largest))

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target, multiplier = 1):
        target.rect.move_ip(self.state.x / multiplier, self.state.y)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + SCREEN_WIDTH / 2, -t + SCREEN_HEIGHT / 2

    l = max(-(camera.width - SCREEN_WIDTH), l) 
    t = max((camera.height - SCREEN_HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(0, t + 100)  # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


class Player(sprite.Sprite):
    def __init__(self, x, y, charType, spawn):
        sprite.Sprite.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.inv = False
        self.isVisible = True
        self.isHurt = False
        self.isStunned = False
        self.isCrouching = False
        self.isParrying = False
        self.isCountering = False
        self.isSliding = False
        self.isJumping = False
        self.isAttacking = False
        self.isDamaging = False
        self.onGround = False
        self.onWall = False
        self.parryTick = -1000
        self.hurtTick = -1000
        self.invTick = -4000
        self.invOver = False
        self.stunTick = -500
        self.spawn = spawn
        self.beginning = spawn
        self.won = False
        self.maxhealth = 4
        self.health = self.maxhealth
        self.attack = namespace(rect = Rect(0,0,50,100))
        self.Animations = {
            "Left": {},
            "Right": {}
        }
        self.facing = "Right"
        self.charType = charType
        self.attackCount = 0

        # Загружаем спрайт
        self.sprite_width = 150
        self.sprite_height = 110
        self.image = transform.scale(get_sprite(sheets["Warrior"],0,0,1,1),(self.sprite_width, self.sprite_height))
        self.image.set_colorkey((0, 0, 0))

        # Создаем хитбокс (уменьшим его, чтобы он совпадал с ногами персонажа)
        self.hitbox_width = 50
        self.hitbox_height = 90  # Подкорректируйте, если нужно
        self.startPos = Rect(x, y, self.hitbox_width, self.hitbox_height)
        self.rect = self.startPos

        for direction in ["Left", "Right"]:
            for anim, params in TYPICAL_ANIMS[self.charType].items():
                Animation(self, anim, self.charType, direction, params[0], params[1], params[2])

    def update(self, left, right, up, down, platforms, z, c, enemies):

        if self.isDamaging:
            self.isDamaging = False

        invDiff = time.get_ticks() - self.invTick

        if self.isStunned:
            left = right = up = down = z = c = False

        if invDiff > 3000:
            self.inv = False
            self.isVisible = True
        else:
            if (invDiff // 150) % 2 == 0:
                self.isVisible = False
            else:
                self.isVisible = True

        if self.invOver:
            self.inv = True
        
        if time.get_ticks() - self.parryTick > 300 and self.isParrying:
            self.isParrying = False
            self.isStunned = True
            self.stunTick = time.get_ticks()

        if time.get_ticks() - self.hurtTick > 500:
            self.isHurt = False

        if time.get_ticks() - self.stunTick > 500:
            self.isStunned = False

        if up and self.onGround and not self.isAttacking and not self.isHurt and not self.isCrouching and not self.isSliding and not self.isParrying and not self.isCountering:
            self.yvel = -JUMP_POWER
            self.isJumping = True
            self.playAnim("Jump")
        elif up and self.onWall:
            self.yvel = -JUMP_POWER
            self.xvel = self.xvel = 7 * directions[getOppositeDirection(self.facing)]
            self.facing = getOppositeDirection(self.facing)
            self.isJumping = True
            self.isHurt = True
            self.hurtTick = time.get_ticks()
            self.onWall = False
            self.playAnim("Jump")


        if self.rect.y > 700:
            self.addHealth(-1)
            if self.health > 0:
                self.respawn()
                self.inv = True
                self.invTick = time.get_ticks()
            right = False
            left = False

        if left and not self.isHurt and not self.isCrouching and not self.isSliding and not self.isParrying and not self.isCountering:
            if self.isAttacking:
                if self.isJumping and self.facing == "Left":
                    self.xvel = -MOVE_SPEED
                else:
                    self.xvel = 0
            else:
                if self.onWall and self.facing == "Right":
                    self.onWall = False
                self.xvel = -MOVE_SPEED
                self.facing = "Left"
                self.playAnim("Walk")

        if right and not self.isHurt and not self.isCrouching and not self.isSliding and not self.isParrying and not self.isCountering:
            if self.isAttacking:
                if self.isJumping and self.facing == "Right":
                    self.xvel = MOVE_SPEED
                else:
                    self.xvel = 0
            else:
                if self.onWall and (self.facing == "Left" or self.onGround):
                    self.onWall = False
                self.xvel = MOVE_SPEED
                self.facing = "Right"
                self.playAnim("Walk")

        if not (left or right) and not self.isAttacking and not self.isHurt and not self.isCrouching and not self.isSliding and not self.isParrying and not self.isCountering:
            self.xvel = 0
            self.playAnim("Idle")
            self.onWall = False

        if self.isSliding:
            self.xvel = directions[self.facing] * 10
            self.playAnim("Slide")
            self.rect.height = PLATFORM_HEIGHT
            if not self.Animations[self.facing]["Slide"].isPlaying:
                self.isSliding = False

        if down and not self.isAttacking and not self.isHurt and not self.isJumping and not self.onWall and self.onGround and not self.isSliding and not self.isParrying and not self.isCountering:
            self.xvel = 0
            self.isCrouching = True
            self.playAnim("Crouch")
            self.rect.height = PLATFORM_HEIGHT
            self.rect.bottomleft = (self.rect.x, self.rect.y + self.sprite_height)
            if up:
                self.isCrouching = False
                self.isSliding = True

        if not down:
            self.isCrouching = False

        if not (self.isSliding or self.isCrouching):
            self.rect.height = self.hitbox_height

        if self.onWall:
            global GRAVITY
            GRAVITY = ACTUAL_GRAVITY / 3
        else:
            GRAVITY = ACTUAL_GRAVITY

        self.yvel += GRAVITY

        self.onGround = False
        self.onWall = False

        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms, right, left)

        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms, right, left)

        if self.isJumping and not (self.Animations["Left"]["Jump"].isPlaying or self.Animations["Right"]["Jump"].isPlaying):
            self.playAnim("Fall")
        elif self.isJumping:
            self.playAnim("Jump")

        if z and not self.isAttacking and not self.isHurt and not self.onWall and not self.isSliding:
            self.attackCount += 1
            if self.attackCount == 4: self.attackCount = 1
            self.isAttacking = True
            self.xvel = 0

        if self.isAttacking:
            self.playAnim(f"Attack{self.attackCount}")
            if not self.Animations[self.facing][f"Attack{self.attackCount}"].isPlaying:
                self.isAttacking = False
            
        if c and not self.isAttacking and not self.isHurt and not self.onWall and not self.isSliding:
            self.isParrying = True
            self.isStunned = True
            self.stunTick = time.get_ticks() + 500
            self.parryTick = time.get_ticks()

        if self.isParrying:
            self.playAnim("Parry")

        self.attack.rect.centerx = self.rect.centerx + directions[self.facing] * 50
        self.attack.rect.centery = self.rect.centery - 5
        self.attack.rect.width = 50

        if self.isCountering:
            self.playAnim("Counter")
            self.xvel = directions[self.facing] * 14
            self.attack.rect.centerx = self.rect.centerx + directions[self.facing] * 20
            self.attack.rect.width = 230
            if not self.Animations[self.facing]["Counter"].isPlaying:
                self.isCountering = False
                self.invOver = False

        if self.isHurt:
            if (self.isCrouching or self.isSliding):
                self.rect.bottomleft = (self.rect.x, self.rect.y)
                self.isCrouching = False
                self.isSliding = False
            self.isAttacking = False
            self.onWall = False
            self.playAnim("Jump")

        self.checkDamage(enemies, platforms)
        self.checkItems()

    def playAnim(self, name):
        frame = self.Animations[self.facing][name].play()
        if frame.event:
            frame.event(self)

    def stopAnim(self, name):
        self.Animations[self.facing][name].stop()

    def respawn(self):
        self.rect.x = self.spawn.rect.x
        self.rect.y = self.spawn.rect.y
        self.inv = True
        self.invTick = time.get_ticks()

    def addHealth(self, diff):
        self.health = clamp(self.health + diff, 0, self.maxhealth)

    def collide(self, xvel, yvel, platforms, right, left):
        for p in platforms:
            if sprite.collide_rect(self, p):
                if p.canCollide:
                    if xvel > 0:
                        self.rect.right = p.rect.left
                        if not self.onGround and right and self.yvel >= 0:
                            self.isJumping = False
                            self.onWall = True
                            self.playAnim("WallSlide")
                    if xvel < 0:
                        self.rect.left = p.rect.right
                        if not self.onGround and left and self.yvel >= 0:
                            self.isJumping = False
                            self.onWall = True
                            self.playAnim("WallSlide")
                    if yvel > 0:
                        self.rect.bottom = p.rect.top
                        self.onGround = True
                        self.onWall = False
                        self.isJumping = False
                        self.stopAnim("Jump")
                        self.yvel = GRAVITY
                    if yvel < 0:
                        self.rect.top = p.rect.bottom
                        self.yvel = 0
                elif p.code == "^" and not self.inv and p.isVisible:
                    self.getDamaged()
                elif p.code == "#":
                    self.spawn = p
                elif p.code == "!":
                    self.won = True


    def getDamaged(self):
        self.addHealth(-1)
        self.inv = True
        self.invTick = time.get_ticks()
        self.isHurt = True
        self.hurtTick = time.get_ticks()
        if (self.isCrouching or self.isSliding):
            self.rect.bottomleft = (self.rect.x, self.rect.y)
            self.isCrouching = False
            self.isSliding = False
        self.isAttacking = False
        self.onWall = False
        self.yvel = -7
        self.xvel = 7 * directions[getOppositeDirection(self.facing)]
        

    def checkDamage(self, enemies, platforms = []):
        for e in enemies:
            if sprite.collide_rect(self, e.attack) and e.health > 0 and e.isDamaging:
                if self.isParrying:
                    print("COUNTER")
                    e.isDamaging = False
                    self.isParrying = False
                    self.isCountering = True
                    self.invOver = True
                    self.isStunned = True
                    self.stunTick = time.get_ticks()
                elif not self.inv:
                    self.getDamaged()
            if sprite.collide_rect(self.attack, e) and self.isDamaging and not e.inv and e.health > 0:
                e.addHealth(-1)
                e.inv = True
                e.invTick = time.get_ticks()
                e.isHurt = True
                e.facing = getOppositeDirection(self.facing)
                if e.health <= 0 and self.health < 4:
                    e.spawnItem()
        for p in platforms:
            if sprite.collide_rect(self.attack, p) and p.isDestructable and (self.isDamaging or self.isSliding):
                p.canCollide = False
                p.isVisible = False
            
    def checkItems(self):
        for i in Items:
            if sprite.collide_rect(self, i) and not i.used:
                i.used = True
                self.addHealth(1)


    def draw(self, screen):
        # Рисуем хитбокс (для отладки)
        # pygame.draw.rect(screen, (0, 255, 0), self.rect, 2)  # Зеленый контур хитбокса

        # Смещаем спрайт так, чтобы он находился над хитбоксом
        sprite_x = self.rect.x - (self.sprite_width - self.hitbox_width) // 2
        if self.isCrouching or self.isSliding:
            sprite_y = self.rect.y - (self.sprite_height - self.hitbox_height) - 36
        else:
            sprite_y = self.rect.y - (self.sprite_height - self.hitbox_height) + 2

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
        self.canCollide = True if tile not in cantCollide else False
        self.isDestructable = True if tile in destructable else False
        self.isVisible = True
        self.code = tile
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = transform.scale(get_sprite(tile_sheet, tiles[tile][0], tiles[tile][1], sprite_params["Tile"][0], sprite_params["Tile"][1]),
                                     (PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.set_colorkey((0, 0, 0))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
