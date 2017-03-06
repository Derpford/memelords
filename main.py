from pygame.locals import *
#Import Pygame.
import pygame
import pymunk
import pymunk.pygame_util
#And system libs.
import os, sys, math, random
#And my other files.
import actors, rooms 
from helpers import *
debug=False

#Screen settings.
pygame.init()
#screen = pygame.display.set_mode((400,300),FULLSCREEN)
screen = pygame.display.set_mode((400,300))

#Pymunk debug.
options=pymunk.pygame_util.DrawOptions(screen)
options.positive_y_is_up=True
options.DRAW_SHAPES=True
hudSurface = rooms.hudInit()

clock=pygame.time.Clock()
font=pygame.font.Font(None,16)
keyDelay=0 # Time until next key press can be processed. Only for one-press keys.


def updateFunc(room):
    room.update(t,dt,keyDelay,player)
def drawFunc(roomImg,room):
    room.draw(roomImg,player,screen,clock,fps)

t=0
fps=60
dt=1/60/fps
mapRoom=rooms.gameRoom('assets/rooms/corridor.tmx')
mapImg=pygame.Surface((400,204))
player=actors.Player(mapRoom.space,200,150)
for layer in mapRoom.grid.layers:
    for x, y, img in layer.tiles():
        mapImg.blit(img,(x*16,y*16))

# MAIN LOOP
while 1:
    updateFunc(mapRoom)
    drawFunc(mapImg,mapRoom)

