import pygame, math, random, pytmx, pymunk, sys
from helpers import *
from pygame.locals import *
import hud, bads

debug=False
exitFlag=0

class Room():
    def __init__():
        #Initialize things.
        raise NotImplementedError
    def update():
        #Update things.
        raise NotImplementedError
    def draw():
        #Draw things.
        raise NotImplementedError

class gameRoom(Room):
    def __init__(self,tile):
        self.roomFile=tile
        self.grid=pytmx.load_pygame(tile)
        self.space=pymunk.Space()
        self.space.gravity = 0,0
        self.mapImg=pygame.Surface((400,204))
        self.hudSurface = hud.hudInit()
        self.bads=[]
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
                            box.collison_type=collisionTypes["wall"]
                            body.position=x*16,y*16
                            self.space.add(body,box)
        
        #Adding enemies.
        if 'bads' in self.grid.layernames:
            for obj in self.grid.layernames['bads']:
                props=obj.properties
                if props==None:
                    pass
                else:
                    if "bad" in props:
                        badName=props["bad"]
                        newBad=bads.badList[badName](self.space,obj.x,obj.y)
                        self.bads.append(newBad)


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
            exitFlag=int(exit.body.props['exit'])
            player=arbiter.shapes[1]
            fx,fy=player.body.position
            if 'xflip' in exit.body.props:
                fx = width-fx+(24*exitFlag)
            if 'yflip' in exit.body.props:
                fy = height-fy+(24*exitFlag)
            player.body.jumpTo((fx,fy))
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
        # Iterate through baddies.
        for bad in self.bads:
            bad.update(player)

    # Draw the room.
    def draw(self,player,screen,clock,fps):
        #Pymunk debug.
        self.pymunkoptions=pymunk.pygame_util.DrawOptions(screen)
        self.pymunkoptions.positive_y_is_up=True
        self.pymunkoptions.DRAW_SHAPES=True
        #BG.
        screen.fill((0,0,0))
        screen.blit(self.mapImg,(0,0))
        #Player.
        player.draw(screen)
        #Bad guys.
        for bad in self.bads:
            bad.draw(screen)
        #Debug info.
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
        hud.drawHud(screen,self.hudSurface,(0,204),player)
        if debug:
           self.space.debug_draw(self.pymunkoptions) 
        pygame.display.flip()
