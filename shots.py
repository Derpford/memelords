import math, random, types, pymunk
import actors
from helpers import *
debug=debugFlags["shot"]

class Shot(actors.Actor):
    def __init__(self,space,x,y,fx,fy,speed=160,damage=1,dt=1/120):
        actors.Actor.__init__(self,space,x,y,dt)
        self.shape=pymunk.Circle(self.body,3)
        self.shape.collision_type=collisionTypes["shot"]
        space.add(self.body,self.shape)
        self.anim=[ loadImage('assets/shots/orb1.png'),
                    loadImage('assets/shots/orb2.png'),
                    loadImage('assets/shots/orb3.png'),
                    loadImage('assets/shots/orb4.png')]
        self.face=[fx,fy]
        self.shape.damage=damage
        self.speed=speed
        self.timer=0.70
        self.shape.removeFlag=False

    def update(self):
        # Handle removal.
        self.timer -= self.dt
        if debug:print("Shot timer: "+str(self.timer))
        if self.timer<=0:
            self.shape.removeFlag=True
        if self.body.position.x<0: 
            self.shape.removeFlag=True
            if debug:print("Out of bounds -x")
        if self.body.position.y<0: 
            self.shape.removeFlag=True
            if debug:print("Out of bounds -y")
        if self.body.position.x>width: 
            self.shape.removeFlag=True
            if debug:print("Out of bounds +x")
        if self.body.position.y>height: 
            self.shape.removeFlag=True
            if debug:print("Out of bounds +y")
        actors.Actor.update(self)
        # Apply new movement.
        angle=math.atan2(self.face[1],self.face[0])
        self.dx=math.cos(angle)*self.speed*self.dt*self.xFactor
        self.dy=math.sin(angle)*self.speed*self.dt*self.yFactor
        # Apply force.
        self.body.apply_force_at_local_point((self.dx*actors.factor,self.dy*actors.factor),(0,0))
        # Friction.
        self.frictionUpdate()

    def draw(self,screen):
        pos=(self.body.position.x-3,self.body.position.y-3)
        actors.drawAnimation(screen,self.anim,pos,8,self.t)

# Bad guy shot
class BadShot(Shot):
    def __init__(self,space,x,y,fx,fy,speed=120,damage=1,dt=1/120):
        Shot.__init__(self,space,x,y,fx,fy,speed,damage,dt)
        self.shape.collision_type=collisionTypes["badshot"]
