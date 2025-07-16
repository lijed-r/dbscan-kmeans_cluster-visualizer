import pygame
import random
from config import R

def redraw(win, dots):
    win.fill("white")
    for d in dots:
        pygame.draw.circle(win, d[2], (d[0], d[1]), R)
    pygame.display.flip()

def make_bunch(dots, x, y, n=10, rad=10):
    for _ in range(n):
        dx = random.randint(-rad, rad)
        dy = random.randint(-rad, rad)
        dots.append([x + dx, y + dy, "black"])
