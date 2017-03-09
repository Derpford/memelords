from pygame.locals import *
#Import Pygame.
import pygame
import pymunk
import pymunk.pygame_util
#And system libs.
import os, sys, math, random
#And my other files.
import actors, rooms, hud 
import player, bads
from helpers import *
debug=True

pygame.init()

#Screen settings.
#screen = pygame.display.set_mode((width,height),FULLSCREEN)
screen = pygame.display.set_mode((width,height))


#Rooms to load into the dungeon.
roomSpecials=['assets/rooms/shrine.tmx','assets/rooms/grave.tmx']
roomLayouts=['assets/rooms/corridor.tmx','assets/rooms/corridor2.tmx','assets/rooms/corridor3.tmx']
roomPos=0
roomList=[roomLayouts[random.randint(0,2)],
        roomLayouts[random.randint(0,2)],
        roomLayouts[random.randint(0,2)],
        roomSpecials[random.randint(0,1)],
        roomLayouts[random.randint(0,2)],
        roomLayouts[random.randint(0,2)],
        roomLayouts[random.randint(0,2)],
        roomSpecials[random.randint(0,1)]]

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
print("Entering game in room "+str(mapRoom.roomFile))
playerObject=player.Player(mapRoom.space,200,150)

# MAIN LOOP
while 1:
    updateFunc(mapRoom)
    drawFunc(mapRoom)
    if rooms.exitFlag != 0:
        mapRoom.space.remove(playerObject.body, playerObject.shape)
        roomPos+=rooms.exitFlag
        if roomPos<0:
            roomPos=len(roomList)-1
        if roomPos>=len(roomList):
            roomPos=0
        rooms.exitFlag=0
        if debug:
            print("Room Position: "+str(roomPos))
            print("Room .tmx File: "+str(mapRoom.roomFile))
        mapRoom=loadRoom(roomList[roomPos])
        mapRoom.space.add(playerObject.body, playerObject.shape)

