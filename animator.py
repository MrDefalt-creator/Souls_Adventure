from spritehandler import *
from pygame import *

AnimFrames = {
    "Warrior": {
        "Idle": [(0, 0), (1, 0), (2, 0), (3, 0)],
        "Walk": [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1)],
        "Attack1": [(2, 6), (3, 6), (4, 6), (5, 6), (6, 6)],
        "Attack2": [(0, 7), (1, 7), (2, 7), (3, 7)],
        "Attack3": [(4, 7), (5, 7), (6, 7), (0, 8), (1, 8), (2, 8)],
        "Jump": [(2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (0, 3), (4, 2), (5, 2), (6, 2), (0, 3)],
        "Fall": [(1, 3), (2, 3)]

    },
    "Witch": {

    },
    "Skeleton": {
        "Idle": [(0, 0), (1, 0), (2, 0), (3, 0)],
        "Walk": [(0, 1), (1, 1), (2, 1), (3, 1)],
        "Take_hit": [(0, 2), (1, 2), (2, 2), (3, 2)],
        "Death": [(0, 3), (1, 3), (2, 3), (3, 3)],
    }
}

def getOppositeDirection(string):
    return "Right" if string == "Left" else "Left"

class Animation(sprite.Sprite):
    def __init__(self, target, animName, charType, facing, isLooped, doesLinger, frameTime, scalex=150, scaley=110):
        self.isPlaying = False
        self.animName = animName
        self.charType = charType
        self.facing = facing
        self.isLooped = isLooped
        self.doesLinger = doesLinger
        self.target = target
        self.lastFrame = 0
        self.lastTick = time.get_ticks()
        self.frameTime = frameTime

        self.actual_frames = []
        Anim = AnimFrames[self.charType][self.animName]

        flipped = facing == "Left"

        for frame in Anim:
            newframe = transform.scale(get_sprite(sheets[charType], frame[0], frame[1], sprite_params[charType][0], sprite_params[charType][1], flipped), (scalex, scaley))
            newframe.set_colorkey((0, 0, 0))
            self.actual_frames.append(newframe)
        
        self.target.Animations[self.facing][self.animName] = self

    def play(self):
        self.isPlaying = True
        oppositeAnim = self.target.Animations[getOppositeDirection(self.facing)][self.animName]

        if oppositeAnim.isPlaying:
            self.lastFrame = oppositeAnim.lastFrame
            self.lastTick = oppositeAnim.lastTick
            oppositeAnim.isPlaying = False

        self.target.image = self.actual_frames[self.lastFrame]

        if time.get_ticks() - self.lastTick >= self.frameTime:
            self.lastFrame += 1
            self.lastTick = time.get_ticks()

        if self.lastFrame >= len(self.actual_frames):
            if self.isLooped:
                self.lastFrame = 0
            elif self.doesLinger:
                self.lastFrame = len(self.actual_frames) - 1
                self.target.image = self.actual_frames[self.lastFrame]
            else:
                self.stop()

    def stop(self):
        self.isPlaying = False
        self.lastFrame = 0