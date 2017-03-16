import math, random, types, pymunk
import actors,sound
from helpers import *
debug=debugFlags["pickup"]

class Pickup(actors.Actor):
    def __init__(self, space, x = 0, y = 0, dt = 1/120):
        actors.Actor.__init__(self,space,x,y,dt)
        self.shape=pymunk.Circle(self.body,4)
        self.shape.pickup=self.pickup
        self.shape.collision_type=collisionTypes["pickup"]
        space.add(self.body,self.shape)
        self.anim=[loadImage('assets/rice.png')]
        self.shape.removeFlag=False
        self.name="Jelly Donut"
        
    def pickup(self,other):
        if debugFlags["actor"]:
            print("Pickup grabbed")
        if type(other.heal)==types.MethodType:
            other.heal(1)

    def draw(self,screen):
        pos=self.body.position.x-2,self.body.position.y-2
        actors.drawAnimation(screen,self.anim,pos,8,self.t)
