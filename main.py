#Import Pygame.
from pygame.locals import *
import pygame
import pymunk
import pymunk.pygame_util
import sound
pygame.init()
#And system libs.
import os, sys, math, random, types
#And my other files.
from helpers import *
import actors, rooms, hud 
import player, bads, shots, pickups
debug=debugFlags["main"]


# Functions.
def loadRoom(room):
    return rooms.gameRoom(room)

def updateFunc(room):
    global t,dt
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
roomEnd='assets/rooms/exit-floor1.tmx'
roomLayouts=['assets/rooms/corridor.tmx','assets/rooms/corridor2.tmx','assets/rooms/corridor3.tmx','assets/rooms/chokepoint.tmx']
roomPos=-1

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
    if type(rooms.exitFlag) is str:
        if rooms.exitFlag==QUIT_GAME:
            roomPos=-1
            mapRoom.space.remove(playerObject.body, playerObject.shape)
            playerObject=None
            mapRoom=rooms.menuRoom()
            rooms.exitFlag=0
        if rooms.exitFlag==NEXT_FLOOR:
            global floor
            roomPos=-1
            floor+=1
            print(str(floor)+" floor")
            if playerObject!=None and mapRoom.space!=None:
                mapRoom.space.remove(playerObject.body, playerObject.shape)
                playerObject.body.position=200,150
            rooms.exitFlag=0
            mapRoom=rooms.loadRoom()

        if rooms.exitFlag==LOAD_COMPLETE:
            roomList=mapRoom.newRoomList
            mapRoom=roomList[0]
            if playerObject==None:
                playerObject=player.Player(mapRoom.space,200,150)
            else:
                mapRoom.space.add(playerObject.body, playerObject.shape)
            rooms.exitFlag=0

    if type(rooms.exitFlag) is int:
        if rooms.exitFlag != 0:
            if playerObject!=None:
                mapRoom.space.remove(playerObject.body, playerObject.shape)
            roomPos+=rooms.exitFlag
            if roomPos<0:
                roomPos=len(roomList)-1
            if roomPos>=len(roomList):
                roomPos=0
            rooms.exitFlag=0
            if debug:
                print("Room Position: "+str(roomPos))
                try:print("Room .tmx File: "+str(mapRoom.roomFile))
                except AttributeError:pass
                print("Room list:")
                for room in roomList: print(str(room))
            mapRoom=roomList[roomPos]
            if playerObject==None:
                playerObject=player.Player(mapRoom.space,200,150)
            else:
                mapRoom.space.add(playerObject.body, playerObject.shape)

