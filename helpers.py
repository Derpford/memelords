import pygame, math, random

pygame.font.init()
# Font.
font=pygame.font.Font(None,16)
gameFont=pygame.font.Font('assets/fonts/Px437_ToshibaLCD_8x8.ttf',8)
textColors={ "dark":(41,57,65),
        "light":(186,195,117),
        "medlight":(133,149,80),
        "meddark":(72,93,72),
        }

def textMultiLine(font,text,color,bg=textColors["dark"],color2=None):
    textList=text.split('\n')
    # Determine height and width of surface to draw to.
    sizex,sizey=0,0
    for line in textList:
        sx,sy=font.size(line)
        if sx>sizex:sizex=sx #Widest line.
        sizey+=sy#Number of lines.
    finalSurface=pygame.Surface((sizex,sizey))
    finalSurface.fill(bg)
    # Now render the strings.
    lineY=0
    for line in textList:
        sx,sy=font.size(line)
        if lineY==0 and color2!=None:
            blit=font.render(line,False,color2)
        else:
            blit=font.render(line,False,color)
        finalSurface.blit(blit,(0,lineY))
        lineY+=sy
    return finalSurface


keyDelayMax=0.01 # Time until next key press can be processed. Only for one-press keys.
# Pseudo-Normalize a number.
def normal(num):
    if num!=0:
        return num/abs(num)
    else: return 0

# Width/Height constants.
width=400
height=300
scale = 1 # Set this to change window from pix-perfect to pix-double, etc

# Collision types.
collisionTypes={
        "player":1,
        "exit":2,
        "bad":3,
        "shot":4,
        "badshot":5,
        "wall":6,
        "pickup":7,
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

# Debug values.
debugFlags={"room":False,
        "input":False,
        "actor":False,
        "weapon":False,
        "shot":False,
        "player":False,
        "bad":False,
        "main":False,
        "physics":False,
        "anim":False,
        "pickup":False,
        }
# Time vars.
t=0
fps=60
dt=1/60/fps
# Room counter.
roomPos=-1
# Floor counter.
floor=0
def floorAdd(num):
    global floor
    floor+=num
def floorGet():
    global floor
    return floor
def floorSet(num):
    global floor
    floor=num

# Quit check constant.
QUIT_GAME="quit"
# New floor constant.
NEXT_FLOOR="floor"
LOAD_COMPLETE="load"
