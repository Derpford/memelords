import math, random
import actors
from helpers import *
debug=True

class Shot(Actor):
    def __init__(self,space,x=0,y=0,fx,fy,dt=1/120):
        Actor.__init__(self,space,x,y,dt)
        self.anim=['assets/shots/orb1.png',
                    'assets/shots/orb2.png',
                    'assets/shots/orb3.png',
                    'assets/shots/orb4.png']
        self.face=[fx,fy]
        self.damage=1

