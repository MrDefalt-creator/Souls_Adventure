import pygame
from pygame import *
from mainclasses import *
from spritehandler import *
from animator import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, charType, spawn):
        sprite.Sprite.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.spawn = spawn
        self.inv = False
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
        self.image = transform.scale(
            get_sprite(sheets[charType], warrior[0][0], warrior[0][1], sprite_params[charType][0], sprite_params[charType][1]),
            (self.sprite_width, self.sprite_height)
        )
        self.image.set_colorkey((0, 0, 0))
        self.hitbox_width = 80
        self.hitbox_height = 120
        self.startPos = Rect(x, y, self.hitbox_width, self.hitbox_height)
        self.rect = self.startPos  
        for direction in ["Left", "Right"]:
            for anim, params in TYPICAL_ANIMS[self.charType].items():
                Animation(self, anim, self.charType, direction, params[0], params[1], params[2], self.sprite_width, self.sprite_height)
    
    def update(self, platforms):

        self.playAnim("Idle")
    
        if not self.onGround:
            self.yvel += GRAVITY

        self.onGround = False
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)
    
    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p) and p.canCollide:
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

    def playAnim(self, name):
        self.Animations[self.facing][name].play()

    def stopAnim(self, name):
        self.Animations[self.facing][name].stop()
    
    def addHealth(self, diff):
        self.health = clamp(self.health + diff, 0, self.maxhealth)

    def draw(self, screen):
        # Рисуем хитбокс (для отладки)
        # pygame.draw.rect(screen, (0, 255, 0), self.rect, 2)  # Зеленый контур хитбокса

        # Смещаем спрайт так, чтобы он находился над хитбоксом
        sprite_x = self.rect.x - (self.sprite_width - self.hitbox_width) // 2
        sprite_y = self.rect.y - (self.sprite_height - self.hitbox_height) // 2 - 5

        # Рисуем спрайт поверх хитбокса
        screen.blit(self.image, (sprite_x, sprite_y))
    
