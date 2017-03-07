import pygame, math, random, pytmx, pymunk, sys
from helpers import *
from pygame.locals import *

debug=True
hudSurface=None
barSprites=None
heartSprites=None
exitFlag=0
# Hud surface and sprites.
def hudInit():
    global heartSprites, barSprites, hudSurface
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

def drawHud(screen,surf,pos,player):
    screen.blit(surf,pos)
    for i in range(0,player.maxhp):
        if i >= player.hp:
            screen.blit(barSprites[1],tupSum(pos,(16+i*4,16)))
        else:
            screen.blit(barSprites[0],tupSum(pos,(16+i*4,16)))

class Room():
    def __init__():
        #Initialize things.
        raise NotImplemented
    def update():
        #Update things.
        raise NotImplemented
    def draw():
        #Draw things.
        raise NotImplemented

class gameRoom(Room):
    def __init__(self,tile):
        Room.__init__()
        self.grid=pytmx.load_pygame(tile)
        self.space=pymunk.Space()
        self.space.gravity = 0,0
        self.mapImg=pygame.Surface((400,204))
        # Tiled iterators.
        #Adding the tile bounding boxes.
        if 'tiles' in self.grid.layernames:
            for x,y,img in self.grid.layernames['tiles'].tiles():
                # Tile bounding boxes.
                    props = self.grid.get_tile_properties(x,y,0)
                    if props==None:
                        pass
                    else:
                        if "solid" in props:
                            body=pymunk.Body(1,1,pymunk.Body.STATIC)
                            box=pymunk.Poly(body,[(0,0),(0,16),(16,16),(16,0)])
                            body.position=x*16,y*16
                            self.space.add(body,box)
        



        #Adding exits.
        if 'exits' in self.grid.layernames:
            for obj in self.grid.layernames['exits']:
                # Exit bounding boxes.
                if debug:
                    print(str(obj))
                props = obj.properties
                body=pymunk.Body(1,1,pymunk.Body.STATIC)
                body.sensor=True
                body.props=props
                box=pymunk.Poly(body,obj.points)
                box.collision_type=collisionTypes["exit"]
                self.space.add(body,box)
        #Adding the stuff in the 'tiles' layer to the screen.
        if 'tiles' in self.grid.layernames:
            for x, y, img in self.grid.layernames['tiles'].tiles():
                self.mapImg.blit(img,(x*16,y*16))

        # Exit handler.
        def exitRoom(arbiter,space,data):
            global exitFlag
            if debug:
                print("Exiting room!")
            exit=arbiter.shapes[0]
            player=arbiter.shapes[1]
            fx,fy=player.body.position
            if exit.body.props['xflip']==True:
                fx = width-fx+16
            if exit.body.props['yflip']==True:
                fy = height-fy+16
            player.body.jumpTo((fx,fy))
            exitFlag=int(exit.body.props['exit'])
            if debug:
                print("Exit num:"+str(exitFlag))
                print("Xflip: "+str(exit.body.props['xflip'])+", new X: "+str(player.body.position.x))
                print("New X should be: "+str(fx))
                print("Yflip: "+str(exit.body.props['yflip'])+", new Y: "+str(player.body.position.y))
                print("New Y should be: "+str(fy))

            return True

        h = self.space.add_collision_handler(
                collisionTypes["exit"],
                collisionTypes["player"])
        h.begin = exitRoom
            


    # Update the room.
    def update(self,t,dt,keyDelay,player):
        t+=dt
        # Step through simulation.
        self.space.step(dt)
        if keyDelay>0:
            keyDelay=max(0,keyDelay-dt)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        player.update(self)
        if pygame.key.get_pressed()[K_q] and keyDelay==0:
            player.hurt(1)
            keyDelay=0.25
        if pygame.key.get_pressed()[K_h] and keyDelay==0:
            player.heal(1)
            keyDelay=0.25
        if pygame.key.get_pressed()[K_ESCAPE]:
            sys.exit()

    def draw(self,player,screen,clock,fps):
        #Pymunk debug.
        self.pymunkoptions=pymunk.pygame_util.DrawOptions(screen)
        self.pymunkoptions.positive_y_is_up=True
        self.pymunkoptions.DRAW_SHAPES=True
        screen.fill((0,0,0))
        screen.blit(self.mapImg,(0,0))
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
           self.space.debug_draw(self.pymunkoptions) 
        pygame.display.flip()
