import math, random, types, pymunk
import actors
from helpers import *
debug=False

class Shot(actors.Actor):
    def __init__(self,space,x,y,fx,fy,dt=1/120):
        actors.Actor.__init__(self,space,x,y,dt)
        self.shape=pymunk.Circle(self.body,1)
        self.shape.collision_type=collisionTypes["shot"]
        space.add(self.body,self.shape)
        self.anim=[ loadImage('assets/shots/orb1.png'),
                    loadImage('assets/shots/orb2.png'),
                    loadImage('assets/shots/orb3.png'),
                    loadImage('assets/shots/orb4.png')]
        self.face=[fx,fy]
        self.shape.damage=1
        self.speed=160
        self.shape.removeFlag=False
        def hitEnemy(arbiter,space,data):
            other=arbiter.shapes[1]
            shot=arbiter.shapes[0]
            if type(other.hurt)==types.MethodType:
                other.hurt(shot.damage)
            shot.removeFlag=True
            return True
        def hitShot(arbiter,space,data):
            other=arbiter.shapes[1]
            shot=arbiter.shapes[0]
            for body in space.bodies:
                if math.hypot(other.position.x-shot.position.x,other.position.y-shot.position.y)<8:
                    body.apply_impulse_at_world_point(40*actors.factor,shot.position)
            shot.removeFlag=True
            other.removeFlag=True
            return False
        def hitWall(arbiter,space,data):
            shot=arbiter.shapes[0]
            shot.removeFlag=True
            return False
        def hitPlayer(arbiter,space,data):
            return False
        space.add_collision_handler(collisionTypes["shot"], collisionTypes["bad"]).begin=hitEnemy
        space.add_collision_handler(collisionTypes["shot"], collisionTypes["wall"]).begin=hitWall
        space.add_collision_handler(collisionTypes["shot"], collisionTypes["exit"]).begin=hitWall
        space.add_collision_handler(collisionTypes["shot"], collisionTypes["player"]).begin=hitPlayer
        space.add_collision_handler(collisionTypes["shot"], collisionTypes["badshot"]).begin=hitShot
        space.add_collision_handler(collisionTypes["shot"], collisionTypes["shot"]).begin=hitPlayer

    def update(self):
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
        pos=self.body.position.x-2,self.body.position.y-2
        actors.drawAnimation(screen,self.anim,pos,8,self.t)
