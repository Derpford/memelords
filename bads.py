import math, random
import actors
from helpers import *

class Bad(actors.Actor):
    def init(self,space,x=0,y=0,dt=1/120):
        actors.Actor.__init__(space,x,y,dt)
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
        self.face=[0,1]
        self.speed=120
        self.dx=0
        self.dy=0
        self.hp=3
        self.maxhp=3
        self.dead=False
        self.pattern=[(1,0),(-1,0)]
        self.patternTimer=0.5
        self.patternTimerMax=0.5
        self.patternStep=-1

    def update(self):
        self.t+=self.dt
        self.patternTimer-=dt
        if self.patternTimer<0:
            self.patternStep+=1
            dx, dy=self.pattern[self.patternStep]
            self.face=[dx,dy]
            self.patternTimer=self.patternTimerMax

        angle=math.atan2(self.face[1],self.face[0])
        self.dx=math.cos(angle)*self.speed*self.dt*self.xFactor
        self.dy=math.sin(angle)*self.speed*self.dt*self.yFactor
        self.body.apply_force_at_local_point((self.dx*actors.factor,self.dy*actors.factor),(0,0))

    def draw(self,screen):
        pos=(self.body.position.x-8,self.body.position.y-8)
        if self.pattern[self.patternStep]!=(0,0):
            # Walking.
            if self.face[0]!=0:
                if self.face[0]>0:
                    actors.drawAnimation(screen,self.anim[4:6],pos,8*abs(self.face[0]),self.t)
                if self.face[0]<0:
                    actors.drawAnimation(screen,self.anim[7:9],pos,8*abs(self.face[0]),self.t)
            else:
                if self.face[1]<0:
                    actors.drawAnimation(screen,self.anim[10:12],pos,8*abs(self.face[1]),self.t)
                else:
                    actors.drawAnimation(screen,self.anim[1:3],pos,8*abs(self.face[1]),self.t)
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
