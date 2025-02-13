import time

import pygame
from pygame import *
from mainclasses import *
from spritehandler import *
from animator import *
from Heal import Heal
from random import *
from types import SimpleNamespace as namespace

MOVE_SPEED = 2

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, charType, spawn):
        sprite.Sprite.__init__(self)
        self.tick = time.get_ticks() + randint(0, 12000)
        self.xvel = 0
        self.yvel = 0
        self.spawn = spawn
        self.isHurt = False
        self.isAttacking = False
        self.isDamaging = False
        self.hurtTick = -1000
        self.inv = False
        self.invTick = -1000
        self.maxhealth = 4
        self.health = self.maxhealth
        self.onGround = False
        self.Animations = {
            "Left": {},
            "Right": {}
        }
        self.facing = "Left"
        self.charType = charType

        # Загружаем спрайт
        self.sprite_width = 370
        self.sprite_height = 370
        self.image = transform.scale(get_sprite(sheets["Warrior"],0,0,1,1),(self.sprite_width, self.sprite_height))
        self.image.set_colorkey((0, 0, 0))
        self.hitbox_width = 80
        self.hitbox_height = 120
        self.startPos = Rect(x, y, self.hitbox_width, self.hitbox_height)
        self.rect = self.startPos  
        self.attack = namespace(rect = Rect(self.rect.x + directions[self.facing] * 90, self.rect.y, 200, self.hitbox_height))
        for direction in ["Left", "Right"]:
            for anim, params in TYPICAL_ANIMS[self.charType].items():
                Animation(self, anim, self.charType, direction, params[0], params[1], params[2], self.sprite_width, self.sprite_height)
    
    def update(self, platforms, hero):
    
        self.attack.rect.centerx = self.rect.centerx + directions[self.facing] * 90
        self.attack.rect.centery = self.rect.centery

        self.isDamaging = False

        if time.get_ticks() - self.invTick > 200:
            self.inv = False

        self.playAnim("Idle")

        if not self.isHurt and self.health <= 0:
            self.playAnim("Death")
    
        if not self.onGround:
            self.yvel += GRAVITY

        if not self.inv and not self.health <= 0 and not self.isHurt and not self.isAttacking:
            self.do_something()
        else:
            self.xvel = 0

        if self.isAttacking and not self.health <= 0:
            self.playAnim("Attack")
            if not self.Animations[self.facing]["Attack"].isPlaying:
                self.isAttacking = False

        if self.isHurt and self.health >= 0:
            self.playAnim("Take_hit")
            if not self.Animations[self.facing]["Take_hit"].isPlaying:
                self.isHurt = False

        self.checkHero(hero)

        self.onGround = False
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)

        self.image = self.image.convert_alpha()

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):
                if p.canCollide:
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
                elif p.code == "*":
                    if xvel > 0:
                        self.rect.right = p.rect.left - 1
                    if xvel < 0:
                        self.rect.left = p.rect.right + 1

    def playAnim(self, name):
        frame = self.Animations[self.facing][name].play()
        if frame.event:
            frame.event(self)

    def stopAnim(self, name):
        self.Animations[self.facing][name].stop()
    
    def addHealth(self, diff):
        self.health = clamp(self.health + diff, 0, self.maxhealth)

    def checkHero(self, hero):
        if sprite.collide_rect(self.attack, hero) and not self.isAttacking and not self.health <= 0 and not self.isHurt:
            self.facing = getOppositeDirection(hero.facing)
            self.isAttacking = True

    def spawnItem(self):
        Heal(self)

    def draw(self, screen):
        # Рисуем хитбокс (для отладки)
        # pygame.draw.rect(screen, (0, 255, 0), self.rect, 2)  # Зеленый контур хитбокса

        # Смещаем спрайт так, чтобы он находился над хитбоксом
        sprite_x = self.rect.x - (self.sprite_width - self.hitbox_width) // 2
        sprite_y = self.rect.y - (self.sprite_height - self.hitbox_height) // 2 - 5

        #draw.rect(screen, (255,0,0), self.attack.rect, 3)

        # Рисуем спрайт поверх хитбокса
        screen.blit(self.image, (sprite_x, sprite_y))

    def do_something(self):
        diff = time.get_ticks() - self.tick
        match (diff // 3000) % 4:
            case 0:
                self.xvel = -MOVE_SPEED
                self.facing = "Left"
                self.playAnim("Walk")
            case 1:
                self.xvel = 0
                self.facing = "Left"
                self.playAnim("Idle")
            case 2:
                self.xvel = MOVE_SPEED
                self.facing = "Right"
                self.playAnim("Walk")
            case 3:
                self.xvel = 0
                self.facing = "Right"
                self.playAnim("Idle")