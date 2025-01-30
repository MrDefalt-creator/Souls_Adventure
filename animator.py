from spritehandler import *
from dataclasses import dataclass
from pygame import *

@dataclass
class Animation(sprite.Sprite):
    target: sprite.Sprite
    frames: list

    actual_frames = []
