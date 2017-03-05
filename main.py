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



# Hud surface and sprites.
heartSprites = [loadImage('assets/hud/heart1.png'),loadImage('assets/hud/heart2.png'),loadImage('assets/hud/heart2.png')]
barSprites =[loadImage('assets/hud/bar1.png'),loadImage('assets/hud/bar2.png')] 
hudSurface = pygame.Surface((400,96))
hudSprites = loadImage('assets/hud/bg.png')
hudTopSprite = pygame.Surface((384,8))
hudBottomSprite = pygame.Surface((384,8))
hudLeftSprite = pygame.Surface((8,80))
hudRightSprite = pygame.Surface((8,80))
hudSurface.fill((133,149,80))
hudSurface.blit(hudSprites,(0,0),pygame.Rect(0,0,8,8))
hudSurface.blit(hudSprites,(392,0),pygame.Rect(24,0,8,8))
hudSurface.blit(hudSprites,(0,88),pygame.Rect(0,24,8,8))
hudSurface.blit(hudSprites,(392,88),pygame.Rect(24,24,8,8))

# Top, Bottom, Left and Right sides
for i in range(0,math.floor(384/16)):
    hudTopSprite.blit(hudSprites,(i*16,0),pygame.Rect(8,0,16,8))
for i in range(0,math.floor(384/16)):
    hudBottomSprite.blit(hudSprites,(i*16,0),pygame.Rect(8,24,16,8))
for i in range(0,math.floor(80/16)):
    hudLeftSprite.blit(hudSprites,(0,i*16),pygame.Rect(0,8,8,16))
for i in range(0,math.floor(80/16)):
    hudRightSprite.blit(hudSprites,(0,i*16),pygame.Rect(24,8,8,16))
hudSurface.blit(hudTopSprite,(8,0))
hudSurface.blit(hudBottomSprite,(8,88))
hudSurface.blit(hudLeftSprite,(0,8))
hudSurface.blit(hudRightSprite,(392,8))

clock=pygame.time.Clock()
font=pygame.font.Font(None,16)
keyDelay=0 # Time until next key press can be processed. Only for one-press keys.

def drawHud(screen,surf,pos,player):
    screen.blit(surf,pos)
    for i in range(0,player.maxhp):
        if i >= player.hp:
            screen.blit(barSprites[1],tupSum(pos,(16+i*4,16)))
        else:
            screen.blit(barSprites[0],tupSum(pos,(16+i*4,16)))

def updateFunc(room):
    global t, dt, keyDelay
    t+=dt
    # Step through simulation.
    room.space.step(dt)
    if keyDelay>0:
        keyDelay=max(0,keyDelay-dt)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    player.update(room)
    if pygame.key.get_pressed()[K_q] and keyDelay==0:
        player.hurt(1)
        keyDelay=0.25
    if pygame.key.get_pressed()[K_h] and keyDelay==0:
        player.heal(1)
        keyDelay=0.25
    if pygame.key.get_pressed()[K_ESCAPE]:
        sys.exit()

def drawFunc(roomImg,room):
    screen.fill((0,0,0))
    screen.blit(roomImg,(0,0))
    player.draw(screen)
    fpsReal=getfps(clock,fps)
    if debug:
        fpsBlit=font.render(str(math.floor(fpsReal)),False,(255,255,255))
        hpBlit=font.render(str(player.hp),False,(255,0,0))
        velBlit=font.render(str(math.floor(player.dx))+" dx/"+str(math.floor(player.dy))+" dy",False,(255,255,255))
        forBlit=font.render(str(math.floor(player.body.force.x))+","+str(math.floor(player.body.force.y)),False,(0,255,255))
        screen.blit(fpsBlit,(0,0))
        screen.blit(hpBlit,(0,16))
        screen.blit(velBlit, (0,24))
        screen.blit(forBlit, (0,32))
    drawHud(screen,hudSurface,(0,204),player)
    if debug:
       room.space.debug_draw(options) 
    pygame.display.flip()




t=0
fps=60
dt=1/60/fps
mapRoom=rooms.Room('assets/rooms/corridor.tmx')
mapImg=pygame.Surface((400,204))
player=actors.Player(mapRoom.space,200,150)
for layer in mapRoom.grid.layers:
    for x, y, img in layer.tiles():
        mapImg.blit(img,(x*16,y*16))


while 1:
    updateFunc(mapRoom)
    drawFunc(mapImg,mapRoom)
