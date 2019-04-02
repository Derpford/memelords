import pygame, math, random, pymunk, sys, types
import  PyTMX as pytmx
import os
from helpers import *
from pygame.locals import *
import hud, bads, actors, sound, player
debug=debugFlags["room"]

exitFlag=0

# Room Dictionary.
roomDict = {}

def registerRoom(room,name,category=roomDict):
    # Add a room to the global room list.
    category[name]=room
    print("Registered "+name+" room.")

# Register the default rooms.
registerRoom('assets/rooms/start.tmx',"start1")
registerRoom('assets/rooms/start-floor2.tmx',"start2")
registerRoom('assets/rooms/exit-floor1.tmx',"exit1")
registerRoom('assets/rooms/exit-floor2.tmx',"exit2")
registerRoom('assets/rooms/corridor.tmx',"corridor")
registerRoom('assets/rooms/corridor2.tmx',"corridor2")
registerRoom('assets/rooms/corridor3.tmx',"corridor3")
registerRoom('assets/rooms/corridor4.tmx',"corridor4")
registerRoom('assets/rooms/shrine.tmx',"shrine")
registerRoom('assets/rooms/chokepoint.tmx',"chokepoint")
registerRoom('assets/rooms/grave.tmx',"grave")
registerRoom('assets/rooms/tunnel.tmx',"tunnel")
registerRoom('assets/rooms/tunnel2.tmx',"tunnel2")
registerRoom('assets/rooms/tunnel3.tmx',"tunnel3")
registerRoom('assets/rooms/tunnel4.tmx',"tunnel4")
registerRoom('assets/rooms/tunnel5.tmx',"tunnel5")
## Floor 1.
## Floor 2

def makeRoomList(roomSet,specialRoomSet,start,end,length,freq):
    newList=[]
    for i in range(0,length):
        if i==0:
            newRoom = roomDict[start]
            if debug:print("Start room!")
        if i==length-1:
            newRoom = roomDict[end]
            if debug:print("End room!")
        if i>0 and i<length-1:
            if i%freq==0:
                newRoom = roomDict[random.choice(specialRoomSet)]
            else:
                newRoom = roomDict[random.choice(roomSet)]
        if os.path.isfile(newRoom):
            newList.append(gameRoom(newRoom))
            print("Loaded "+str(newRoom))
        else:
            print("Missing file "+str(newRoom))
    return newList


class Room():
    def __init__():
        #Initialize things.
        raise NotImplementedError
    def update(self,t,dt,player):
        #Update things.
        raise NotImplementedError
    def draw(self,player,screen,clock,fps):
        #Draw things.
        raise NotImplementedError



class loadRoom(Room):
    def __init__(self):
        self.bg=loadImage('assets/load.png')
        self.newRoomList=[]

    def update(self,t,dt,player):
        global exitFlag
        roomSpecials1=['shrine','chokepoint','grave']
        roomStart1='start1'
        roomEnd1='exit1'
        roomLayouts1=['corridor','corridor2','corridor3','corridor4']
        roomStart2='start2'
        roomLayouts2=['tunnel','tunnel2','tunnel3','tunnel4','tunnel5']
        roomEnd2='exit2'

        if floorGet()==1 and exitFlag==0:
            self.newRoomList=makeRoomList(roomLayouts1,roomSpecials1,roomStart1,roomEnd1,10,4)
        if floorGet()==2 and exitFlag==0:
            self.newRoomList=makeRoomList(roomLayouts2,roomLayouts2,roomStart2,roomEnd2,10,4)
        if floorGet()==3 and exitFlag==0:
            #End.
            self.newRoomList=[creditsRoom()]
        exitFlag=LOAD_COMPLETE

            

    def draw(self,player,screen,clock,fps):
        screen.fill((0,0,0))
        screen.blit(self.bg,(0,0))

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
        exitFlag=NEXT_FLOOR
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
                    sound.sounds["shot"].play()

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
        self.grid=pytmx.TiledMap(tile)
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
                        #newBad=bads.badList[badName](self,obj.x+8,obj.y+8)
                        # Now we do it with the actor list.
                        newBad=actors.actorDict[badName](self,obj.x+8,obj.y+8)
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
            for x, y, pic in self.grid.layernames['tiles'].tiles():
                img = loadImage(pic[0]) # PyTMX now returns a tup
                self.mapImg.blit(img,(x*16,y*16))

        # Exit handler.
        def exitRoom(arbiter,space,data):
            global exitFlag
            if debug:
                print("Exiting room!")
            exit=arbiter.shapes[0]
            try: exitFlag=int(exit.body.props['exit'])
            except ValueError: exitFlag=exit.body.props['exit']
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
            if shot.removeFlag != None:shot.removeFlag=True
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
                if shot.removeFlag != None:shot.removeFlag=True
            if other.collision_type==collisionTypes["shot"] or other.collision_type==collisionTypes["badshot"]:
                if other.removeFlag != None:other.removeFlag=True
            return False
        def hitWall(arbiter,space,data):
            shot=arbiter.shapes[0]
            if shot.removeFlag != None:shot.removeFlag=True
            sound.sounds["hurt"].play()
            return False
        def hitFriend(arbiter,space,data):
            return False
        def hitPickup(arbiter,space,data):
            item=arbiter.shapes[0]
            other=arbiter.shapes[1]
            item.pickup(other)
            sound.sounds["pick"].play()
            if item.removeFlag != None:item.removeFlag=True
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
                if item.shape.removeFlag: #and item.shape.collision_type !=collisionTypes["player"]:
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

class creditsRoom(Room):
    def __init__(self):
        self.usequence=[]
        self.textpos=100,150
        self.dsequence=[ 
                (0,lambda screen:screen.blit(self.ThankYou(textColors["meddark"]),self.textpos)),
                (0.5,lambda screen:screen.blit(self.ThankYou(textColors["medlight"]),self.textpos)),
                (1,lambda screen:screen.blit(self.ThankYou(textColors["light"]),self.textpos)),
                (2,lambda screen:screen.blit(self.ThankYou(textColors["medlight"]),self.textpos)),
                (2.5,lambda screen:screen.blit(self.ThankYou(textColors["meddark"]),self.textpos)),
                (3,lambda screen:screen.blit(self.ThankYou(textColors["dark"]),self.textpos)),
                (3.5,lambda screen:screen.blit(self.LoonyThanks(textColors["meddark"]),self.textpos)),
                (4,lambda screen:screen.blit(self.LoonyThanks(textColors["medlight"]),self.textpos)),
                (4.5,lambda screen:screen.blit(self.LoonyThanks(textColors["light"]),self.textpos)),
                (6.5,lambda screen:screen.blit(self.LoonyThanks(textColors["medlight"],textColors["light"]),self.textpos)),
                (7,lambda screen:screen.blit(self.LoonyThanks(textColors["meddark"],textColors["light"]),self.textpos)),
                (7.5,lambda screen:screen.blit(self.LoonyThanks(textColors["dark"],textColors["light"]),self.textpos)),
                (8,lambda screen:screen.blit(self.OpenThanks(textColors["meddark"],textColors["light"]),self.textpos)),
                (8.5,lambda screen:screen.blit(self.OpenThanks(textColors["medlight"],textColors["light"]),self.textpos)),
                (9,lambda screen:screen.blit(self.OpenThanks(textColors["light"],textColors["light"]),self.textpos)),
                (11,lambda screen:screen.blit(self.OpenThanks(textColors["meddark"],textColors["light"]),self.textpos)),
                (11.5,lambda screen:screen.blit(self.OpenThanks(textColors["dark"],textColors["light"]),self.textpos)),
                (12,lambda screen:screen.blit(self.InfiniteThanks(textColors["meddark"],textColors["light"]),self.textpos)),
                (12.5,lambda screen:screen.blit(self.InfiniteThanks(textColors["medlight"],textColors["light"]),self.textpos)),
                (13,lambda screen:screen.blit(self.InfiniteThanks(textColors["light"],textColors["light"]),self.textpos)),
                (15,lambda screen:screen.blit(self.InfiniteThanks(textColors["medlight"]),self.textpos)),
                (15.5,lambda screen:screen.blit(self.InfiniteThanks(textColors["meddark"]),self.textpos)),
                (16,lambda screen:screen.blit(self.InfiniteThanks(textColors["dark"]),self.textpos)),
                (16.5,lambda screen:screen.blit(self.EndText(textColors["meddark"]),self.textpos)),
                (17,lambda screen:screen.blit(self.EndText(textColors["medlight"]),self.textpos)),
                (17.5,lambda screen:screen.blit(self.EndText(textColors["light"]),self.textpos)),
                ]
        self.ucurrent=None
        self.dcurrent=None
        self.t=0
    
    def ThankYou(self,color,color2=None):
        return textMultiLine(gameFont,"Thanks for playing!\nTotal money: "+str(self.money),color,textColors["dark"],color2)

    def LoonyThanks(self,color,color2=None):
        return textMultiLine(gameFont,"Special thanks to\n Lunacy--Coding Advice",color,textColors["dark"],color2)

    def InfiniteThanks(self,color,color2=None):
        return textMultiLine(gameFont,"Special thanks to\n InfinityJam",color,textColors["dark"],color2)

    def OpenThanks(self,color,color2=None):
        return textMultiLine(gameFont,"Special thanks to\n OpenGameArt.org",color,textColors["dark"],color2)

    def EndText(self,color,color2=None):
        return textMultiLine(gameFont,"Press any key\nto go back to\n  the  menu",color,textColors["dark"],color2)

    def update(self,t,dt,player):
        self.t+=dt*24
        if player!=None:
            self.money=player.money
        else:
            self.money=0
        global exitFlag
        self.ucurrent=None
        for i in self.usequence:
            if i[0]<=t:
                self.ucurrent=i[1]
        if self.ucurrent!=None:
            self.ucurrent()
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                exitFlag=QUIT_GAME

    def draw(self,player,screen,clock,fps):
        screen.fill(textColors["dark"])
        self.dcurrent=None
        for i in self.dsequence:
            if self.t>=i[0]:
                self.dcurrent=i[1]
        if self.dcurrent!=None:
            self.dcurrent(screen)
        pass

