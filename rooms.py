import pygame, math, random, pytmx, pymunk, sys, types
from helpers import *
from pygame.locals import *
import hud, bads, actors, sound, player
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

class menuRoom(Room):
    def __init__(self):
        self.menu=[("START",self.startGame),("QUIT",self.quit)]
        self.menuPos=0
        self.keyDelay=0
        self.menuBG=loadImage('assets/title.png')
        pass

    def quit(self):
        pygame.quit()
        sys.exit()

    def startGame(self):
        global exitFlag
        exitFlag=1
        print(str(exitFlag))
    
    def update(self,t,dt,player):
        self.keyDelay=max(0,self.keyDelay-dt)
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key==K_UP and self.keyDelay==0:
                    self.menuPos-=1
                    if self.menuPos<0:
                        self.menuPos=len(self.menu)-1
                    self.keyDelay=self.keyDelay
                    sound.sounds["boop"].play()
                if event.key==K_DOWN and self.keyDelay==0:
                    self.menuPos+=1
                    if self.menuPos>=len(self.menu):
                        self.menuPos=0
                    self.keyDelay=self.keyDelay
                    sound.sounds["boop"].play()
                if event.key==K_LCTRL and self.keyDelay==0:
                    self.menu[self.menuPos][1]()
                    self.keyDelay=self.keyDelay

    def draw(self,player,screen,clock,fps):
        global t,dt
        t+=dt
        screen.fill((0,0,0))
        screen.blit(self.menuBG,(0,0))
        pos=(150,150)
        for i in self.menu:
            menuBlit=gameFont.render(i[0],False,textColors["dark"])
            screen.blit(menuBlit,tupSum(pos,(0,self.menu.index(i)*16)))
        if t*12%2>1:
            selBlit=loadImage('assets/guy-green/guy-green5.png')
        else:
            selBlit=loadImage('assets/guy-green/guy-green6.png')
        screen.blit(selBlit,tupSum(pos,(-16,self.menuPos*16))) 

class gameRoom(Room):
    def __init__(self,tile):
        self.pause=False
        self.roomFile=tile
        self.keyDelay=0
        self.grid=pytmx.load_pygame(tile)
        self.space=pymunk.Space()
        self.space.gravity = 0,0
        self.mapImg=pygame.Surface((400,204))
        self.hudSurface = hud.hudInit()
        self.bads=[]
        self.drops=[]
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
                        newBad=bads.badList[badName](self,obj.x+8,obj.y+8)
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
            if debugFlags["physics"]:print("Collision between "+str(shot.collision_type)+" and "+str(other.collision_type))
            if type(other.hurt)==types.MethodType:
                other.hurt(shot.damage)
            shot.removeFlag=True
            return True
        def hitShot(arbiter,space,data):
            other=arbiter.shapes[1]
            shot=arbiter.shapes[0]
            sound.pingChannel.play(sound.sounds["ping"])
            if debugFlags["physics"]:print("Collision between "+str(shot.collision_type)+" and "+str(other.collision_type))
            for body in space.bodies:
                if abs(math.hypot(body.position.x-shot.body.position.x,body.position.y-shot.body.position.y))<8:
                    #body.apply_impulse_at_world_point(40*actors.factor,shot.body.position)
                    dx=800*actors.factor*normal(body.position.x-shot.body.position.x)
                    dy=800*actors.factor*normal(body.position.y-shot.body.position.y)
                    body.apply_impulse_at_world_point((dx,dy),shot.body.position)
            if shot.collision_type==collisionTypes["shot"] or shot.collision_type==collisionTypes["badshot"]:
                shot.removeFlag=True
            if other.collision_type==collisionTypes["shot"] or other.collision_type==collisionTypes["badshot"]:
                other.removeFlag=True
            return False
        def hitWall(arbiter,space,data):
            shot=arbiter.shapes[0]
            shot.removeFlag=True
            sound.sounds["hurt"].play()
            return False
        def hitFriend(arbiter,space,data):
            return False
        def hitPickup(arbiter,space,data):
            item=arbiter.shapes[0]
            other=arbiter.shapes[1]
            item.pickup(other)
            item.removeFlag=True
            return False

        self.space.add_collision_handler(collisionTypes["pickup"],collisionTypes["player"]).begin=hitPickup
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
    def update(self,t,dt,player):
        self.keyDelay=max(0,self.keyDelay-dt)
        t+=dt
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if debug or debugFlags["input"]: print("Got event: "+str(event.type)+","+str(event.key))
                if event.key==K_ESCAPE and self.keyDelay==0:
                    self.pause = not self.pause
                    self.keyDelay=keyDelayMax
                if event.key==K_q and self.pause:
                    print("Quitting")
                    global exitFlag
                    exitFlag=QUIT_GAME
        if not self.pause:
            # Step through simulation.
            self.space.step(dt)
            player.update(self)
            # Iterate through baddies.
            for bad in self.bads:
                bad.update(self,player)
            for item in self.drops:
                if item.shape.removeFlag:
                    self.space.remove(item.shape)
                    self.space.remove(item.body)
                    self.drops.remove(item)
                item.update()

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
        for item in self.drops:
            item.draw(screen)
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
        if self.pause:
            pauseBlit=gameFont.render("PAUSED",False,textColors["light"])
            screen.blit(pauseBlit,(180,140))
