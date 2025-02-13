import time

from pygame import *
from spritehandler import *
from animator import *
from random import *
from types import SimpleNamespace as namespace
from mainclasses import *
from tweenService import Tween
from projectile import *

class Witch(sprite.Sprite):
    def __init__(self, x, y, charType):
        sprite.Sprite.__init__(self)
        self.tick = time.get_ticks()
        self.xvel = 0
        self.yvel = 0
        self.isHurt = False
        self.isAttacking = False
        self.isDamaging = False
        self.hurtTick = -1000
        self.attackCD = False
        self.attackTick = -1000
        self.inv = False
        self.invTick = -1000
        self.maxhealth = 15
        self.health = self.maxhealth
        self.cutscene = True
        self.action = 0
        self.onGround = False
        self.Animations = {
            "Left": {},
            "Right": {}
        }
        self.facing = "Left"
        self.charType = charType

        # Загружаем спрайт
        self.sprite_width = 112
        self.sprite_height = 168
        self.image = transform.scale(get_sprite(sheets["Warrior"],0,0,1,1),(self.sprite_width, self.sprite_height))
        self.image.set_colorkey((0, 0, 0))
        self.hitbox_width = 80
        self.hitbox_height = 90
        self.startPos = Rect(x, y, self.hitbox_width, self.hitbox_height)
        self.rect = self.startPos  
        self.attack = namespace(rect = Rect(self.rect.x + directions[self.facing] * 90, self.rect.y, 200, self.hitbox_height))
        for direction in ["Left", "Right"]:
            for anim, params in TYPICAL_ANIMS[self.charType].items():
                Animation(self, anim, self.charType, direction, params[0], params[1], params[2], self.sprite_width, self.sprite_height)
        
        self.tweens = [
            Tween(self, Rect(100, 300, 0, 0), 0.5),
            Tween(self, Rect(100, 400, 0, 0), 0.5),
            Tween(self, Rect(1100, 300, 0, 0), 0.5),
            Tween(self, Rect(1100, 400, 0, 0), 0.5)
        ]

        shuffle(self.tweens)

        self.spikes = []

        for _ in range(5):
            x = randint(20, 1240)
            self.spikes.append(Projectile((Rect(x, -100, 40, 90), Rect(x, 800, 40, 90), 2, "Ice2", "Right", self)))
        
        self.startTween = Tween(self, Rect(1100, 400, 0, 0), 2)
        
    def update(self, platforms, hero):
        self.playAnim("Idle")

        if time.get_ticks() - self.invTick > 200:
            self.inv = False

        if time.get_ticks() - self.attackTick > 500:
            self.attackCD = False

        if not self.onGround:
            self.yvel += GRAVITY

        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)

        if not self.cutscene and self.health > 0:
            self.do_something()
            for spike in self.spikes:
                if not spike.active and not self.attackCD:
                    spike.active = True
                    self.attackCD = True
                    self.attackTick = time.get_ticks()

                if spike.destroyed:
                    x = randint(20, 1240)
                    spike.rect = Rect(x, -100, 40, 90)
                    spike.finish = Rect(x, 800, 40, 90)
                    spike.updateTween()
                    spike.active = False
                    spike.destroyed = False
                    spike.collided = False

        else:
            self.startTween.play()
            self.playAnim("Fly")
            if self.startTween.isFinished:
                self.cutscene = False
                self.tick = time.get_ticks()
                self.tweens[0].update(self)

        if self.isHurt:
            self.playAnim("Take_hit")
            if not self.Animations[self.facing]["Take_hit"].isPlaying:
                self.isHurt = False

        if not self.isHurt and self.health <= 0:
            self.playAnim("Death")
            self.yvel += GRAVITY
            if not hero.end:
                hero.end = True
                hero.endTick = time.get_ticks()
        
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

    def playAnim(self, name):
        frame = self.Animations[self.facing][name].play()
        if frame.event:
            frame.event(self)

    def addHealth(self, diff):
        self.health = clamp(self.health + diff, 0, self.maxhealth)

    def draw(self, screen):
        # draw.rect(screen, (255, 0, 0), self.rect, 3)  # Зеленый контур хитбокса

        sprite_x = self.rect.x - (self.sprite_width - self.hitbox_width) // 2
        sprite_y = self.rect.y - (self.sprite_height - self.hitbox_height) // 2 - 10

        #draw.rect(screen, (255,0,0), self.attack.rect, 3)

        screen.blit(self.image, (sprite_x, sprite_y))

    def spawnItem(self):
        ""

    def resetTweens(self, exception):
        for t in self.tweens:
            if t != exception:
                t.isFinished = False
                t.lastFrame = 0
                t.update(self)
    
    def do_something(self):
        diff = time.get_ticks() - self.tick

        if (diff // 3000) % 4 != self.action and self.action == 3:
            lastaction = self.tweens[3]
            shuffle(self.tweens)
            if self.tweens == lastaction:
                shuffle(self.tweens) # Двойная перемешка, меньший шанс повтора

        self.action = (diff // 3000) % 4

        number = self.action
        self.resetTweens(self.tweens[number])
        self.facing = "Left" if self.rect.x > 640 else "Right" # Всегда смотреть в сторону центра экрана

        if not self.tweens[number].isFinished:
            self.tweens[number].play()
        else:
            self.isAttacking = True

        match number:
            case 0:
                self.playAnim("Fly")
            case 1:
                self.playAnim("Fly")
            case 2:
                self.playAnim("Fly")
            case 3:
                self.playAnim("Fly")