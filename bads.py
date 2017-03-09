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
            self.dx, self.dy=self.pattern[self.patternStep]
            self.patternTimer=self.patternTimerMax
        self.body.apply_force_at_local_point((self.dx*actors.factor,self.dy*actors.factor),(0,0))

