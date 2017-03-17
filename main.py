from pygame.locals import *
#Import Pygame.
import pygame
import pymunk
import pymunk.pygame_util
pygame.init()
#And system libs.
import os, sys, math, random
#And my other files.
from helpers import *
import actors, rooms, hud 
import player, bads, shots, pickups
import sound
debug=debugFlags["main"]


# Functions.
def loadRoom(room):
    return rooms.gameRoom(room)

def updateFunc(room):
    global t,dt,keyDelay
    if keyDelay>0:
        keyDelay=max(0,keyDelay-dt)
    t+=dt
    global roomPos
    for event in pygame.event.get(pygame.QUIT):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    room.update(t,dt,playerObject)
        
def drawFunc(room):
    room.draw(playerObject,screen,clock,fps)

#Screen settings.
#screen = pygame.display.set_mode((width,height),FULLSCREEN)
screen = pygame.display.set_mode((width,height))


#Rooms to load into the dungeon.
roomSpecials=['assets/rooms/shrine.tmx','assets/rooms/grave.tmx']
roomStart='assets/rooms/start.tmx'
roomLayouts=['assets/rooms/corridor.tmx','assets/rooms/corridor2.tmx','assets/rooms/corridor3.tmx','assets/rooms/chokepoint.tmx']
roomPos=0
roomList=[loadRoom(roomStart),
        loadRoom(random.choice(roomLayouts)),
        loadRoom(random.choice(roomLayouts)),
        loadRoom(random.choice(roomLayouts)),
        #loadRoom(random.choice(roomSpecials)),
        loadRoom(roomSpecials[0]),
        loadRoom(random.choice(roomLayouts)),
        loadRoom(random.choice(roomLayouts)),
        loadRoom(random.choice(roomLayouts)),
        loadRoom(random.choice(roomSpecials))]


clock=pygame.time.Clock()

playerObject=None

#mapRoom=rooms.gameRoom(roomLayouts[random.randrange(len(roomLayouts))])
mapRoom=rooms.menuRoom()
print("Entering game in room "+str(mapRoom))

# MAIN LOOP
while 1:
    updateFunc(mapRoom)
    drawFunc(mapRoom)
    pygame.display.flip()
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
        mapRoom=roomList[roomPos]
        mapRoom.space.add(playerObject.body, playerObject.shape)

