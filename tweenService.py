from pygame import *

def lerp(times, points, steps):
    divisor = steps-1
    dt =     (times[1] - times[0]) / divisor
    dx = (points[1][0] - points[0][0]) / divisor
    dy = (points[1][1] - points[0][1]) / divisor
    t, x, y = (times[0],) + points[0]
    for _ in range(steps):
        yield t, x, y
        t += dt
        x += dx
        y += dy

class Tween(sprite.Sprite):
    def __init__(self, target, start, finish, duration):
        self.target = target
        self.start = start
        self.finish = finish
        self.lastFrame = 0
        self.tick = -1000
        self.isFinished = False
        self.duration = duration
        self.timing = duration * 10
        self.frames = []

        x_1, y_1 = self.start.x, self.start.y
        x_2, y_2 = self.finish.x, self.finish.y
        times = [1, 100]
        points = [(x_1, y_1), (x_2, y_2)]
        steps = times[1] - times[0] + 1
        for _, x, y in lerp(times, points, steps):
            self.frames.append((x, y))
    
    def play(self):
        self.target.rect.x = self.frames[self.lastFrame][0]
        self.target.rect.x = self.frames[self.lastFrame][1]

        if time.get_ticks() - self.tick > self.timing:
            self.lastFrame += 1

        if self.lastFrame > 100:
            self.isFinished = True