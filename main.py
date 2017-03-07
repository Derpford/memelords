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
debug=True

pygame.init()

#Screen settings.
#screen = pygame.display.set_mode((width,height),FULLSCREEN)
screen = pygame.display.set_mode((width,height))

hudSurface = rooms.hudInit()

#Rooms to load into the dungeon.
roomLayouts=['assets/rooms/corridor.tmx','assets/rooms/shrine.tmx','assets/rooms/grave.tmx']
roomPos=0
roomList=[roomLayouts[0],roomLayouts[1]]

clock=pygame.time.Clock()
keyDelay=0 # Time until next key press can be processed. Only for one-press keys.

def loadRoom(room):
    return rooms.gameRoom(room)

def updateFunc(room):
    global roomPos
    room.update(t,dt,keyDelay,playerObject)
        
def drawFunc(room):
    room.draw(playerObject,screen,clock,fps)

t=0
fps=60
dt=1/60/fps
#mapRoom=rooms.gameRoom(roomLayouts[random.randrange(len(roomLayouts))])
mapRoom=loadRoom(roomList[0])
print("Entering game in room "+str(roomList[0]))
playerObject=player.Player(mapRoom.space,200,150)

# MAIN LOOP
while 1:
    updateFunc(mapRoom)
    drawFunc(mapRoom)
    if rooms.exitFlag != 0:
        mapRoom.space.remove(playerObject.body, playerObject.shape)
        roomPos+=rooms.exitFlag
        if roomPos<0:
            roomPos=len(roomList)
        if roomPos>len(roomList):
            roomPos=0
        rooms.exitFlag=0
        if debug:
            print(str(roomPos-1))
            print(str(roomList[roomPos-1]))
        mapRoom=loadRoom(roomList[roomPos-1])
        mapRoom.space.add(playerObject.body, playerObject.shape)

