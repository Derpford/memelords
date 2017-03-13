import math, random, pymunk
import actors
from helpers import *
debug=False

class Bad(actors.Actor):
    def __init__(self,space,x=0,y=0,dt=1/120):
        actors.Actor.__init__(self,space,x,y,dt)
        self.shape=pymunk.Circle(self.body,8)
        space.add(self.body,self.shape)
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
        self.shape.collision_type = collisionTypes["bad"]
        self.shape.hurt=self.hurt
        self.face=[0,0]
        self.speed=120
        self.animSpeed=8
        self.dx=0
        self.dy=0
        self.hp=3
        self.maxhp=3
        self.dead=False
        self.pattern=[(1,0),(0,0),(-1,0),(0,0)]
        self.patternTimer=1
        self.patternTimerMax=0.5
        self.patternStep=-1

    def update(self,player):
        if self.hp<1:
            self.dead=True
        if not self.dead:
            actors.Actor.update(self)
            self.patternTimer-=self.dt
            if self.patternTimer<0:
                self.patternStep+=1
                if self.patternStep>=len(self.pattern):
                    self.patternStep=0
                dx, dy=self.pattern[self.patternStep]
                self.face=[dx,dy]
                self.patternTimer=self.patternTimerMax

            angle=math.atan2(self.face[1],self.face[0])
            self.dx=math.cos(angle)*self.speed*self.dt*self.xFactor
            self.dy=math.sin(angle)*self.speed*self.dt*self.yFactor
            if self.face!=[0,0]:
                self.body.apply_force_at_local_point((self.dx*actors.factor,self.dy*actors.factor),(0,0))
        self.frictionUpdate()

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

    def hurt(self,amount):
        if debug: print(self.name+" got hurt for "+str(amount))
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

class Knight(Bad):
    def __init__(self,space,x=0,y=0,dt=1/120):
        Bad.__init__(self,space,x,y,dt)
        self.name="Knight"
        self.speed=80
        self.animSpeed=4
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

    def update(self,player):
        actors.Actor.update(self)
        self.t+=self.dt
        tpos = player.body.position
        spos = self.body.position
        self.face=[normal(tpos[0]-spos[0]),normal(tpos[1]-spos[1])]
        angle = math.atan2(tpos[1]-spos[1],tpos[0]-spos[0])
        self.dx=math.cos(angle)*self.speed*self.dt*self.xFactor
        self.dy=math.sin(angle)*self.speed*self.dt*self.yFactor
        self.body.apply_force_at_local_point((self.dx*actors.factor,self.dy*actors.factor),(0,0))
        self.frictionUpdate()



#List of bad guy classes.
badList={"hood":Hood,"knight":Knight}
