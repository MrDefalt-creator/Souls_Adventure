from spritehandler import *
from pygame import *

# TODO:
# Добавить в Player свойство facing, определяет последний поворот в сторону
# Добавить в Player свойство state, определяет получение урона, смерть и т.д.
# Добавить в Player свойство hp, объяснения не требуются
#

Animations = {
    # Крч, этот словарь должен быть перенесен в класс Player. В Player вызывается класс Animation и туда передаются нужные данные для анимации, потом сам класс заносится в этот словарь под ключом - именем анимации.
    "Warrior": [],
    "Witch": []
}

AnimFrames = {
    "Warrior": {
        "Idle": [(0, 0), (1, 0), (2, 0), (3, 0)],
        "Walk": [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1)],
        "Attack": [
            [(2, 6), (3, 6), (4, 6), (5, 6), (6, 6)],
            [(0, 7), (1, 7), (2, 7), (3, 7)],
            [(4, 7), (5, 7), (6, 7), (0, 8), (1, 8), (2, 8)]
        ],
        "Jump": [(2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (0, 3), (1, 3), (2, 3)],

    },
    "Witch": {

    }
}


class Animation(sprite.Sprite):
    def __init__(self, animName, charType, facing, isLooped, doesLinger):
        self.isPlaying = "False"
        self.animName = animName
        self.charType = charType
        self.facing = facing
        self.isLooped = isLooped
        self.doesLinger = doesLinger

        actual_frames = []
        Anim = AnimFrames[self.charType][self.animName]

        flipped = facing == "Left"

        for frame in Anim:
            newframe = transform.scale(get_sprite(sheets[charType], frame[0], frame[1], sprite_params[charType][0], sprite_params[charType][1], flipped), (150, 110))
            newframe.set_colorkey((0, 0, 0))
            actual_frames.append(newframe)

    def play(self):
        self.isPlaying = True

    def stop(self):
        self.isPlaying = False