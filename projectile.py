from pygame import *
from spritehandler import *
from animator import *
from random import *
from types import SimpleNamespace as namespace
from mainclasses import *
from tweenService import Tween

Projectiles = []

class Projectile(sprite.Sprite):
    def __init__(self, info):
        sprite.Sprite.__init__(self)
        self.rect, self.finish, self.duration, self.pType, self.facing, self.owner = info
        self.tween = Tween(self, self.finish, self.duration)
        self.active = False
        self.collided = False
        self.destroyed = False
        self.sprite_width = 576
        self.sprite_height = 576
        self.hitbox_width = 40
        self.hitbox_height = 90

        self.startPos = Rect(self.rect.x, self.rect.y, self.hitbox_width, self.hitbox_height)
        self.rect = self.startPos 

        self.Animations = {
            "Left": {},
            "Right": {},
        }

        vertical = self.facing == "Left"
        for direction in ["Left", "Right"]:
            for anim, params in TYPICAL_ANIMS[self.pType].items():
                Animation(self, anim, self.pType, direction, params[0], params[1], params[2], self.sprite_width, self.sprite_height, vertical)

        self.image = self.Animations["Right"]["Idle"].actual_frames[0].image.convert_alpha()

        Projectiles.append(self)

    def update(self, platforms, hero):
        if self.active:
            self.tween.play()

            self.playAnim("Idle")

            if self.collided:
                self.playAnim("Destroy")
                if not self.Animations[self.facing]["Destroy"].isPlaying:
                    self.destroyed = True

            self.collide(platforms, hero)

            self.image = self.image.convert_alpha()

    def updateTween(self):
        self.tween = Tween(self, self.finish, self.duration)

    def collide(self, platforms, hero):
        for p in platforms:
            if sprite.collide_rect(self, p):
                if p.canCollide:
                    self.collided = True
            
        if sprite.collide_rect(self, hero):
            if not hero.inv and not self.collided:
                self.collided = True
                hero.getDamaged()

    def playAnim(self, name):
        frame = self.Animations[self.facing][name].play()
        if frame.event:
            frame.event(self)
        
    def draw(self, screen):
        #draw.rect(screen, (255, 0, 0), self.rect, 3)  # Зеленый контур хитбокса

        sprite_x = self.rect.x - (self.sprite_width - self.hitbox_width) // 2 + 1
        sprite_y = self.rect.y - (self.sprite_height - self.hitbox_height) // 2 + 5

        #draw.rect(screen, (255,0,0), self.attack.rect, 3)

        screen.blit(self.image, (sprite_x, sprite_y))
