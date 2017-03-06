import pygame, math, random

pygame.font.init()
# Font.
font=pygame.font.Font(None,16)

# Width/Height constants.
width=400
height=300

# Collision types.
collisionTypes={
        "player":1,
        "exit":2
        }

# Image Loader.
def loadImage(path):
    return pygame.image.load(path).convert()

# FPS getter.
def getfps(clock,fps=None):
    if fps:
        clock.tick(fps)
    else:
        clock.tick()
    return clock.get_fps()
# Tuple adder.
def tupSum(tup1, tup2):
    return tuple(map(lambda x, y: x + y, tup1,tup2))


