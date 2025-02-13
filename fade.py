from pygame import *
from EndScreen import death_screen, win_screen
from mainclasses import *
from types import SimpleNamespace as namespace
from tweenService import Tween

fade = namespace(rect = Rect(0, -980, 1280, 720), image = fadeImage.convert_alpha())
fadeInTween = Tween(fade, Rect(0, 0, 1280, 720), 1)
fadeOutTween = Tween(fade, Rect(0, -980, 1280, 720), 1)

def fadein(screen):
    if not fadeInTween.isFinished:
        fadeInTween.play()
        print("PLAYING")
        return fadeInTween
    else:
        return False

def fadeout(screen):
    if not fadeOutTween.isFinished:
        fadeOutTween.play()
        return fadeOutTween
    else:
        return False


def reset(screen):
    global fade, fadeInTween, fadeOutTween
    fade = namespace(rect=Rect(0, -980, 1280, 720), image=fadeImage.convert_alpha())
    fadeInTween = Tween(fade, Rect(0, 0, 1280, 720), 0.5)
    fadeOutTween = Tween(fade, Rect(0, -980, 1280, 720), 0.5)