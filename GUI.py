from pygame import *
from spritehandler import *

class GUI(sprite.Sprite):
    def __init__(self, target, camera):
        sprite.Sprite.__init__(self)
        self.rect = Rect(10,10,0,0).move(camera.state.topleft)
        self.hero = target
        self.camera = camera
        self.frames = []
        for spr in health:
            frame = get_sprite(health_sheet, spr[0], spr[1], sprite_params["Health"][0], sprite_params["Health"][1]).convert_alpha()
            frame = transform.scale(frame, (320, 80))
            frame.set_colorkey((0,0,255))
            self.frames.append(frame)

        self.image = self.frames[target.health]

    def update(self):
        self.image = self.frames[self.hero.health]
