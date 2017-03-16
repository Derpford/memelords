import pygame, math, random, pytmx, pymunk, sys, types
from helpers import *
from pygame.locals import *
import hud, bads, actors, sound
debug=debugFlags["room"]

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
                            body.position=x*16,y*16
                            self.space.add(body,box)
                            box.collision_type=collisionTypes["wall"]
                            if debug:
                                print("Made a wall at "+str(body.position)+" with collision type "+str(box.collision_type))
        
        #Adding enemies.
        if 'bads' in self.grid.layernames:
            for obj in self.grid.layernames['bads']:
                props=obj.properties
                if props==None:
                    pass
                else:
                    if "bad" in props:
                        badName=props["bad"]
                        newBad=bads.badList[badName](self.space,obj.x+8,obj.y+8)
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
            player.newRoomFlag=True
            if debug:
                print("Exit num:"+str(exitFlag))
                print("Xflip: "+str(exit.body.props['xflip'])+", new X: "+str(player.body.position.x))
                print("New X should be: "+str(fx))
                print("Yflip: "+str(exit.body.props['yflip'])+", new Y: "+str(player.body.position.y))
                print("New Y should be: "+str(fy))

            return False
        
        #Shot handlers.
        def hitEnemy(arbiter,space,data):
            other=arbiter.shapes[1]
            shot=arbiter.shapes[0]
            if type(other.hurt)==types.MethodType:
                other.hurt(shot.damage)
            shot.removeFlag=True
            return True
        def hitShot(arbiter,space,data):
            other=arbiter.shapes[1]
            shot=arbiter.shapes[0]
            for body in space.bodies:
                if abs(math.hypot(body.position.x-shot.body.position.x,body.position.y-shot.body.position.y))<8:
                    #body.apply_impulse_at_world_point(40*actors.factor,shot.body.position)
                    dx=800*actors.factor*normal(body.position.x-shot.body.position.x)
                    dy=800*actors.factor*normal(body.position.y-shot.body.position.y)
                    body.apply_impulse_at_world_point((dx,dy),shot.body.position)
            shot.removeFlag=True
            other.removeFlag=True
            return False
        def hitWall(arbiter,space,data):
            shot=arbiter.shapes[0]
            shot.removeFlag=True
            sound.sounds["hurt"].play()
            return False
        def hitFriend(arbiter,space,data):
            return False

        self.space.add_collision_handler(collisionTypes["shot"], collisionTypes["badshot"]).begin=hitShot
        #For player shots.
        self.space.add_collision_handler(collisionTypes["shot"], collisionTypes["bad"]).begin=hitEnemy
        self.space.add_collision_handler(collisionTypes["shot"], collisionTypes["wall"]).begin=hitWall
        self.space.add_collision_handler(collisionTypes["shot"], collisionTypes["exit"]).begin=hitWall
        self.space.add_collision_handler(collisionTypes["shot"], collisionTypes["player"]).begin=hitFriend
        self.space.add_collision_handler(collisionTypes["shot"], collisionTypes["shot"]).begin=hitFriend
        #For enemy shots.
        self.space.add_collision_handler(collisionTypes["badshot"],collisionTypes["bad"]).begin=hitFriend
        self.space.add_collision_handler(collisionTypes["badshot"], collisionTypes["wall"]).begin=hitWall
        self.space.add_collision_handler(collisionTypes["badshot"], collisionTypes["exit"]).begin=hitWall
        self.space.add_collision_handler(collisionTypes["badshot"], collisionTypes["player"]).begin=hitEnemy
        self.space.add_collision_handler(collisionTypes["badshot"], collisionTypes["badshot"]).begin=hitFriend
        # For exits.
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
        player.update(self)
        if pygame.key.get_pressed()[K_q] and keyDelay==0:
            player.hurt(1)
            keyDelay=0.25
        if pygame.key.get_pressed()[K_h] and keyDelay==0:
            player.heal(1)
            keyDelay=0.25
        if pygame.key.get_pressed()[K_ESCAPE]:
            sys.exit()
            pygame.quit()
        # Iterate through baddies.
        for bad in self.bads:
            bad.update(self.space,player)

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
            shotTimerBlit=font.render(str(player.weaponAnim)+" shotTimer",False,(255,0,0))
            screen.blit(fpsBlit,(0,0))
            screen.blit(hpBlit,(0,16))
            screen.blit(velBlit, (0,24))
            screen.blit(forBlit, (0,32))
            screen.blit(shotTimerBlit, (0,48))
        hud.drawHud(screen,self.hudSurface,(0,204),player)
        if debug or debugFlags["physics"]:
           self.space.debug_draw(self.pymunkoptions) 
        pygame.display.flip()
