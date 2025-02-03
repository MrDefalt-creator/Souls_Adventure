from pygame import *

Items = []

class Heal(sprite.Sprite):
    def __init__(self, object):
        sprite.Sprite.__init__(self)
        self.object = object
        self.used = False
        self.rect = Rect(self.object.rect.x, self.object.rect.y + 20, 50, 50)
        self.image = transform.scale(image.load("Assets/UI/Heal.png"), (50, 50))
        Items.append(self)

    def update(self):
        self.rect = Rect(self.object.rect.x, self.object.rect.y + 20, 50, 50)

    def draw(self, screen):
        sprite_x = self.rect.x
        sprite_y = self.rect.y

        # Рисуем спрайт поверх хитбокса
        #draw.rect(screen, (0, 255, 0), self.rect, 2)
        screen.blit(self.image, (sprite_x, sprite_y))

    def clear(self):
        self.used = True

