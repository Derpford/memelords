import math, random, pymunk, pygame
import actors,weapons,sound,pickups
from helpers import *
from pygame.locals import *
debug=debugFlags["bad"]

def chooseDrops(drops,space):
        newItem=None
        for drop in drops:
            item,chance=drop
            roll=random.randrange(0,255)
            if debugFlags["pickup"]:
                print("Dropping item!")
                print(str(roll)+">"+str(chance))
            if roll > chance and newItem==None:
                if debugFlags["pickup"]:print("Dropping a "+str(item))
                newItem=item
        return newItem

class Bad(actors.Actor):
    def __init__(self,space,x=0,y=0,dt=1/120):
        actors.Actor.__init__(self,space,x,y,dt)
        self.shape=pymunk.Circle(self.body,8)
        space.space.add(self.body,self.shape)
        self.anim = [loadImage("assets/hood/hood1.png"),
                loadImage("assets/hood/hood2.png"),
                loadImage("assets/hood/hood3.png"),
                loadImage("assets/hood/hood4.png"),
                loadImage("assets/hood/hood5.png"),
                loadImage("assets/hood/hood6.png"),
                pygame.transform.flip(loadImage("assets/hood/hood4.png"),True,False),
                pygame.transform.flip(loadImage("assets/hood/hood5.png"),True,False),
                pygame.transform.flip(loadImage("assets/hood/hood6.png"),True,False),
                loadImage("assets/hood/hood7.png"),
                loadImage("assets/hood/hood8.png"),
                loadImage("assets/hood/hood9.png")]

        self.deadAnim=actors.makeDeadAnim(self.anim)

        self.drops=[(pickups.Pickup,128)]

        self.shape.collision_type = collisionTypes["bad"]
        self.shape.hurt=self.hurt
        # Basic vars.
        self.face=[0,0]
        self.speed=120
        self.animSpeed=8
        self.dx=0
        self.dy=0
        self.hp=3
        self.maxhp=3
        self.dead=False
        # Pattern settings.
        self.pattern=[(1,0),(0,0),(-1,0),(0,0)]
        self.patternTimer=1
        self.patternTimerMax=0.5
        self.patternStep=-1
        # Weapon settings.
        self.weapon=weapons.BadWeapon()
        self.shotTimer=0
        self.shotList=[]

    def update(self,space,player):
        actors.Actor.update(self)
        if self.hp<1 and not self.dead:
            self.dead=True
            sound.sounds["die"].play()
            item=chooseDrops(self.drops,space.space,)
            if item != None:
                newDrop=item(space.space,self.body.position.x,self.body.position.y)
                space.drops.append(newDrop)
        if not self.dead:
            if self.shotTimer>0:self.shotTimer-=self.dt
            self.patternTimer-=self.dt
            if self.patternTimer<0:
                self.patternStep+=1
                if self.patternStep>=len(self.pattern):
                    self.patternStep=0
                dx, dy=self.pattern[self.patternStep]
                self.face=[dx,dy]
                self.patternTimer=self.patternTimerMax

            angle=math.atan2(self.face[1],self.face[0])
            self.dx=math.cos(angle)*self.speed*self.dt*abs(self.pattern[self.patternStep][0])
            self.dy=math.sin(angle)*self.speed*self.dt*abs(self.pattern[self.patternStep][1])
            if self.face!=[0,0]:
                self.body.apply_force_at_local_point((self.dx*actors.factor,self.dy*actors.factor),(0,0))
        if self.dead and self.anim != self.deadAnim:
            self.anim = self.deadAnim
        # Update shots.
        for shot in self.shotList:
            shot.update()
            if debug:
                print("Handling shot, removeFlag: "+str(shot.shape.removeFlag))
                print("shot position: "+str(shot.body.position))
            if shot.shape.removeFlag == True:
                space.space.remove(shot.body)
                space.space.remove(shot.shape)
        self.shotList=[shot for shot in self.shotList if shot.shape.removeFlag==False]

    def draw(self,screen):
        pos=(self.body.position.x-8,self.body.position.y-8)
        if (self.face[0],self.face[1])!=(0,0):
            # Walking.
            if self.face[0]!=0:
                if self.face[0]>0:
                    actors.drawAnimation(screen,self.anim[4:6],pos,self.animSpeed,self.t)
                if self.face[0]<0:
                    actors.drawAnimation(screen,self.anim[7:9],pos,self.animSpeed,self.t)
            else:
                if self.face[1]<0:
                    actors.drawAnimation(screen,self.anim[10:12],pos,self.animSpeed,self.t)
                else:
                    actors.drawAnimation(screen,self.anim[1:3],pos,self.animSpeed,self.t)
        else:
            # Standing.
            if self.face[0]!=0:
                if self.face[0]>0:
                        screen.blit(self.anim[3],pos)
                if self.face[0]<0:
                        screen.blit(self.anim[6],pos)
            else:
                if self.face[1]<0:
                    screen.blit(self.anim[9],pos)
                else:
                    screen.blit(self.anim[0],pos)
        # Draw shots.
        for shot in self.shotList:
            shot.draw(screen)

    def hurt(self,amount):
        if debug: print(self.name+" got hurt for "+str(amount))
        sound.hurtChannel.play(sound.sounds["hurt"])
        self.hp -= amount


class Hood(Bad):
    # Basic bad guy.
    def __init__(self,space,x=0,y=0,dt=1/120):
        Bad.__init__(self,space,x,y,dt)
        self.name="Hoodlum"
        self.patternTimerMax=0.2
        self.pattern=[(0,0),(0,1),
                (0,0),(1,0),
                (0,0),(0,-1),
                (0,0),(-1,0)]
        self.drops=[(pickups.Money,128),(pickups.Pickup,128)]
    def update(self,space,player):
        Bad.update(self,space,player)
        if not self.dead:
            if self.pattern[self.patternStep]==(0,0) and self.shotTimer<=0:
                tx,ty=player.body.position
                fx,fy=normal(tx-self.body.position.x),normal(ty-self.body.position.y)
                self.weapon.shoot(space.space,self.body.position,(fx,fy),self)
                self.shotTimer=1
                if debug:
                    print("Firing a shot at "+str(self.body.position)+" toward "+str(self.pattern[self.patternStep-1]))

class Knight(Bad):
    def __init__(self,space,x=0,y=0,dt=1/120):
        Bad.__init__(self,space,x,y,dt)
        self.name="Knight"
        self.speed=80
        self.animSpeed=4
        self.hp=6
        self.maxhp=6
        self.anim = [loadImage("assets/knight/knight1.png"),
                loadImage("assets/knight/knight2.png"),
                loadImage("assets/knight/knight3.png"),
                loadImage("assets/knight/knight4.png"),
                loadImage("assets/knight/knight5.png"),
                loadImage("assets/knight/knight6.png"),
                pygame.transform.flip(loadImage("assets/knight/knight4.png"),True,False),
                pygame.transform.flip(loadImage("assets/knight/knight5.png"),True,False),
                pygame.transform.flip(loadImage("assets/knight/knight6.png"),True,False),
                loadImage("assets/knight/knight7.png"),
                loadImage("assets/knight/knight8.png"),
                loadImage("assets/knight/knight9.png")]
        self.deadAnim=actors.makeDeadAnim(self.anim)

    def update(self,space,player):
        Bad.update(self,space,player)
        if not self.dead:
            tpos = player.body.position
            spos = self.body.position
            self.face=[normal(tpos[0]-spos[0]),normal(tpos[1]-spos[1])]
            angle = math.atan2(tpos[1]-spos[1],tpos[0]-spos[0])
            if abs(math.hypot(tpos[0]-spos[0],tpos[1]-spos[1]))>64:
                self.dx=math.cos(angle)*self.speed*self.dt*self.xFactor
                self.dy=math.sin(angle)*self.speed*self.dt*self.yFactor
                self.body.apply_force_at_local_point((self.dx*actors.factor,self.dy*actors.factor),(0,0))
            else:
                self.dx=-math.cos(angle)*self.speed*self.dt*self.xFactor
                self.dy=-math.sin(angle)*self.speed*self.dt*self.yFactor
                self.body.apply_force_at_local_point((self.dx*actors.factor,self.dy*actors.factor),(0,0))

class Skeleton(Bad):
    def __init__(self,space,x=0,y=0,dt=1/120):
        Bad.__init__(self,space,x,y,dt)
        self.name="Skeltan"
        self.speed=100
        self.animSpeed=4
        self.patternTimerMax=0.2
        self.hp=4
        self.maxhp=4
        self.weapon=weapons.BadAxe()
        self.anim = [loadImage("assets/skel/skel1.png"),
                loadImage("assets/skel/skel2.png"),
                loadImage("assets/skel/skel3.png"),
                loadImage("assets/skel/skel4.png"),
                loadImage("assets/skel/skel5.png"),
                loadImage("assets/skel/skel6.png"),
                pygame.transform.flip(loadImage("assets/skel/skel4.png"),True,False),
                pygame.transform.flip(loadImage("assets/skel/skel5.png"),True,False),
                pygame.transform.flip(loadImage("assets/skel/skel6.png"),True,False),
                loadImage("assets/skel/skel7.png"),
                loadImage("assets/skel/skel8.png"),
                loadImage("assets/skel/skel9.png")]
        self.deadAnim=actors.makeDeadAnim(self.anim)

    def update(self,space,player):
        Bad.update(self,space,player)
        if not self.dead and self.pattern[self.patternStep]==(0,0):
            tx,ty = player.body.position
            fx,fy = tx-self.body.position.x,ty-self.body.position.y
            if abs(fx)<abs(fy):
                fx=0
            if abs(fx)>abs(fy):
                fy=0
            if fx!=0:fx=normal(fx)
            if fy!=0:fy=normal(fy)
            self.face=fx,fy
            self.pattern=[(fx,fy),(-fx,-fy),(2*fx,2*fy),(0,0),(0,0)]
        if not self.dead and self.patternStep==3:
            if self.shotTimer<=0:
                self.weapon.shoot(space.space,self.body.position,self.face,self)
                self.shotTimer=1

class Shroom(Bad):
    def __init__(self,space,x=0,y=0,dt=1/120):
        Bad.__init__(self,space,x,y,dt)
        self.name="Marishroom"
        self.speed=80
        self.animSpeed=4
        self.patternTimerMax=0.2
        self.hp=4
        self.maxhp=4
        self.weapon=weapons.BadAxe()
        self.anim = [loadImage("assets/shroom/shroom1.png"),
                loadImage("assets/shroom/shroom2.png"),
                loadImage("assets/shroom/shroom3.png"),
                loadImage("assets/shroom/shroom4.png"),
                loadImage("assets/shroom/shroom5.png"),
                loadImage("assets/shroom/shroom6.png"),
                pygame.transform.flip(loadImage("assets/shroom/shroom4.png"),True,False),
                pygame.transform.flip(loadImage("assets/shroom/shroom5.png"),True,False),
                pygame.transform.flip(loadImage("assets/shroom/shroom6.png"),True,False),
                loadImage("assets/shroom/shroom7.png"),
                loadImage("assets/shroom/shroom8.png"),
                loadImage("assets/shroom/shroom9.png")]
        self.deadAnim=actors.makeDeadAnim(self.anim)

    def update(self,space,player):
        Bad.update(self,space,player)
        if not self.dead:
            tpos = player.body.position
            spos = self.body.position
            self.face=[normal(tpos[0]-spos[0]),normal(tpos[1]-spos[1])]
            angle = math.atan2(tpos[1]-spos[1],tpos[0]-spos[0])
            if abs(math.hypot(tpos[0]-spos[0],tpos[1]-spos[1]))<128:
                self.dx=-math.cos(angle)*self.speed*self.dt*self.xFactor
                self.dy=-math.sin(angle)*self.speed*self.dt*self.yFactor
                self.body.apply_force_at_local_point((self.dx*actors.factor,self.dy*actors.factor),(0,0))
            else:
                self.dx=math.cos(angle)*self.speed*self.dt*self.xFactor
                self.dy=math.sin(angle)*self.speed*self.dt*self.yFactor
                self.body.apply_force_at_local_point((self.dx*actors.factor,self.dy*actors.factor),(0,0))

#List of bad guy classes.
badList={"hood":Hood,"knight":Knight,"skel":Skeleton,}
