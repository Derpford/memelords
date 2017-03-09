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