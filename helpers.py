import pygame, math, random

pygame.font.init()
# Font.
font=pygame.font.Font(None,16)
gameFont=pygame.font.Font('assets/fonts/Px437_ToshibaLCD_8x8.ttf',8)
textColors={ "dark":(41,57,65),
        "light":(186,195,117)
        }

# Normalize a number.
def normal(num):
    return num/abs(num)

# Width/Height constants.
width=400
height=300

# Collision types.
collisionTypes={
        "player":1,
        "exit":2,
        "bad":3,
        "shot":4,
        "badshot":5,
        "wall":6
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


