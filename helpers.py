import pygame, math, random, re

pygame.font.init()
# Font.
font=pygame.font.Font(None,16)
gameFont=pygame.font.Font('assets/fonts/Px437_ToshibaLCD_8x8.ttf',8)
textColors={ "dark":(41,57,65),
        "light":(186,195,117),
        "medlight":(133,149,80),
        "meddark":(72,93,72),
        "red":(204,54,54),
        }

def textMultiLine(font,text,color,color2=textColors["red"],bg=None): # bg = textColors["dark"]
    textList=re.split("(\$.)",text) # The text, containing formatting codes. $ is escape, $$ is $ literal.
    unformattedTextList=re.split("\$n",text) # Split the text at $n to get text with newlines...
    for i in range(0,len(unformattedTextList)): # And then strip out all other formatting, except $$.
        unformattedTextList[i]=re.sub("\$[^\$]",'',unformattedTextList[i])
        unformattedTextList[i]=re.sub("\$\$",'$',unformattedTextList[i]) # Replace $$ with $.
    # Determine height and width of surface to draw to, using unformatted text.
    sizex,sizey=0,0
    for line in unformattedTextList:
        sx,sy=font.size(line)
        if sx>sizex:sizex=sx #Widest line.
        sizey+=sy#Number of lines.
    finalSurface=pygame.Surface((sizex,sizey), pygame.SRCALPHA, 32) # We'll return this later. Setting SRCALPHA and bit depth 32 allows transparent surface.
    if bg != None:
        finalSurface.fill(bg)
    # Now render the strings.
    lineY=0
    lineX=0
    emphatic = False
    for line in textList:
        sx,sy=font.size(line)
        if "$" in line: 
            # Newline.
            if line == "$n":
                lineY+=sy
                lineX=0
            # Emphatic text.
            elif line == "$r":
                emphatic = True
            elif line == "$R":
                emphatic = False
            # Escaped $.
            elif "$$" in line:
                line = re.sub("\$\$","$",line)
                if emphatic:
                    blit=font.render(line,False,color2)
                else:
                    blit=font.render(line,False,color,bg)
                finalSurface.blit(blit,(lineX,lineY))
                lineX+=sx
        else:
            if emphatic:
                blit=font.render(line,False,color2)
            else:
                blit=font.render(line,False,color,bg)
            finalSurface.blit(blit,(lineX,lineY))
            lineX+=sx
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
