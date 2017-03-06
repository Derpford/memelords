from pygame.locals import *
#Import Pygame.
import pygame
import pymunk
import pymunk.pygame_util
#And system libs.
import os, sys, math, random
#And my other files.
import actors, rooms 
import player
from helpers import *
debug=False

#Screen settings.
pygame.init()
#screen = pygame.display.set_mode((width,height),FULLSCREEN)
screen = pygame.display.set_mode((width,height))

#Pymunk debug.
options=pymunk.pygame_util.DrawOptions(screen)
options.positive_y_is_up=True
options.DRAW_SHAPES=True
hudSurface = rooms.hudInit()

#Rooms to load into the dungeon.
roomLayouts=['assets/rooms/corridor.tmx','assets/rooms/shrine.tmx','assets/rooms/grave.tmx']

clock=pygame.time.Clock()
font=pygame.font.Font(None,16)
keyDelay=0 # Time until next key press can be processed. Only for one-press keys.


def updateFunc(room):
    room.update(t,dt,keyDelay,playerObject)
def drawFunc(room):
    room.draw(playerObject,screen,clock,fps)

t=0
fps=60
dt=1/60/fps
#mapRoom=rooms.gameRoom(roomLayouts[random.randrange(len(roomLayouts))])
mapRoom=rooms.gameRoom(roomLayouts[0])
playerObject=player.Player(mapRoom.space,200,150)

# MAIN LOOP
while 1:
    updateFunc(mapRoom)
    drawFunc(mapRoom)

