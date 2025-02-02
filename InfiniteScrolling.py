from pygame import *
from types import SimpleNamespace as namespace

# ДА, Я ЭТУ ФИГНЮ САМ ПИСАЛ БЕЗ ГАЙДОВ

class Scroller(sprite.Sprite):
    def __init__(self, background, target):
        sprite.Sprite.__init__(self)
        self.hero = target
        self.backs = {
            "Left": namespace(rect = Rect(background.rect.x - background.rect.width,0,background.rect.width,background.rect.height)),
            "Center": namespace(rect = background.rect),
            "Right": namespace(rect = Rect(0,0,background.rect.width,background.rect.height).move(background.rect.topleft)),
            "Image": background.image
        }

    def update(self) -> dict:

        self.backs["Left"].rect = Rect(0, 0, self.backs["Center"].rect.width, self.backs["Center"].rect.height).move(self.backs["Center"].rect.x - self.backs["Center"].rect.width, self.backs["Center"].rect.y)
        self.backs["Right"].rect = Rect(0, 0, self.backs["Center"].rect.width, self.backs["Center"].rect.height).move(self.backs["Center"].rect.topright)

        found = False
        for bg in ["Left","Right","Center"]:
            if sprite.collide_rect(self.hero, self.backs[bg]):
                found = True
                if not sprite.collide_rect(self.hero, self.backs["Center"]):
                    self.backs["Center"].rect = self.backs[bg].rect
                    break

        if not found:
            self.backs["Center"].rect.x = self.hero.rect.x

        self.backs["Left"].rect = Rect(0, 0, self.backs["Center"].rect.width, self.backs["Center"].rect.height).move(self.backs["Center"].rect.x - self.backs["Center"].rect.width, self.backs["Center"].rect.y)
        self.backs["Right"].rect = Rect(0, 0, self.backs["Center"].rect.width, self.backs["Center"].rect.height).move(self.backs["Center"].rect.topright)

        return self.backs

