import math, random, types, pymunk
import actors,sound,rooms
from helpers import *
debug=debugFlags["shot"]

class hitSpark(actors.Actor):
    def __init__(self,space,x,y,dt=1/120):
        actors.Actor.__init__(self,space,x,y,dt)
        self.anim=[ loadImage('assets/shots/hitspark1.png'),
                    loadImage('assets/shots/hitspark2.png'),
                    loadImage('assets/shots/hitspark3.png')]
        self.timeUp = 0.15 
        self.animSpeed = 16

    def update(self,mapGrid):
        self.t += self.dt
        if self.t > self.timeUp:
            self.removeFlag = True

    def draw(self,screen):
        pos=(self.body.position.x-8,self.body.position.y-8)
        actors.drawAnimation(screen,self.anim,pos,self.animSpeed,self.t)

class parrySpark(hitSpark):
    def __init__(self,space,x,y,dt=1/120):
        hitSpark.__init__(self,space,x,y,dt)
        self.timeUp = 0.30
        self.anim=[ loadImage('assets/shots/parry1.png'),
                    loadImage('assets/shots/parry2.png'),
                    loadImage('assets/shots/parry3.png'),
                    loadImage('assets/shots/parry4.png'),
                    loadImage('assets/shots/parry5.png'),
                    loadImage('assets/shots/parry6.png'),
                    loadImage('assets/shots/parry7.png')]

class hurtSpark(hitSpark):
    def __init__(self,space,x,y,dt=1/120):
        hitSpark.__init__(self,space,x,y,dt)
        self.timeUp = 0.15
        self.animSpeed = 32
        self.anim=[ loadImage('assets/shots/hurtslash1.png'),
                    loadImage('assets/shots/hurtslash2.png'),
                    loadImage('assets/shots/hurtslash3.png'),
                    loadImage('assets/shots/hurtslash4.png'),
                    loadImage('assets/shots/hurtslash5.png'),
                    loadImage('assets/shots/hurtslash6.png')]
        

class Shot(actors.Actor):
    def __init__(self,space,x,y,fx,fy,speed=160,damage=1,dt=1/120):
        actors.Actor.__init__(self,space,x,y,dt)
        self.shape=pymunk.Circle(self.body,3)
        self.shape.collision_type=collisionTypes["shot"]
        self.shape.collided = False
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
        self.hp = 1
        self.shape.hurt=self.hurt
        self.shape.hit=self.hit
        self.shape.hitWall=self.hitWall
        sound.shotChannel.play(sound.sounds["shot"])


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

    def draw(self,screen):
        pos=(self.body.position.x-3,self.body.position.y-3)
        actors.drawAnimation(screen,self.anim,pos,8,self.t)

    def hurt(self,amount):
        self.shape.removeFlag = True        
        spark = parrySpark(self.space,self.body.position.x,self.body.position.y)
        self.room.addActor(spark)
        sound.pingChannel.play(sound.sounds["ping"])

    def hit(self):
        self.shape.removeFlag = True
        spark = hurtSpark(self.space,self.body.position.x,self.body.position.y)
        self.room.addActor(spark)
        sound.hurtChannel.play(sound.sounds["hurt"])
        #sound.sounds["hurt"].play()

    def hitWall(self):
        self.shape.removeFlag = True
        spark = hitSpark(self.space,self.body.position.x,self.body.position.y)
        self.room.addActor(spark)
        sound.hurtChannel.play(sound.sounds["hurt"])
        
# Bad guy shot
class BadShot(Shot):
    def __init__(self,space,x,y,fx,fy,speed=120,damage=1,dt=1/120):
        Shot.__init__(self,space,x,y,fx,fy,speed,damage,dt)
        self.shape.collision_type=collisionTypes["badshot"]

# Spreader weapon.
class SpreadShot(Shot):
    def __init__(self,space,x,y,fx,fy,speed=160,damage=1,dt=1/120):
        Shot.__init__(self,space,x,y,fx,fy,speed,damage,dt)
        self.timer=0.45
        self.anim=[loadImage('assets/shots/pulser1.png'),
                    loadImage('assets/shots/pulser2.png'),
                    loadImage('assets/shots/pulser3.png'),]

# Spreader sub-shot.
class SubShot(Shot):
    def __init__(self,space,x,y,fx,fy,speed=160,damage=1,dt=1/120):
        Shot.__init__(self,space,x,y,fx,fy,speed,damage,dt)
        self.timer=0.40
        rotation=math.atan2(self.face[0],self.face[1])
        rotation=rotation*180/math.pi
        rotation+=90 #Kludge until I rotate the sprite itself
        self.anim=[pygame.transform.rotate(loadImage('assets/shots/beam1.png'),rotation),
                    pygame.transform.rotate(loadImage('assets/shots/beam2.png'),rotation),
                    pygame.transform.rotate(loadImage('assets/shots/beam3.png'),rotation)]
        #if abs(fy)>abs(fx):
        #    self.anim=[ pygame.transform.rotate(loadImage('assets/shots/beam1.png'),90),
        #            pygame.transform.rotate(loadImage('assets/shots/beam2.png'),90),
        #            pygame.transform.rotate(loadImage('assets/shots/beam3.png'),90),]
        #else:
        #    self.anim=[ loadImage('assets/shots/beam1.png'),
        #            loadImage('assets/shots/beam2.png'),
        #            loadImage('assets/shots/beam3.png'),]

# Spear shot.
class LongShot(Shot):
    def __init__(self,space,x,y,fx,fy,speed=160,damage=1,dt=1/120,multi=2):
        Shot.__init__(self,space,x,y,fx,fy,speed,damage,dt)
        self.timer=1.5
        self.changetime=self.timer-0.45
        self.changed=False
        self.multi=multi
        self.anim=[ loadImage('assets/shots/spinnerdouble1.png'),
                    loadImage('assets/shots/spinnerdouble2.png'),
                    loadImage('assets/shots/spinnerdouble3.png'),
                    loadImage('assets/shots/spinnerdouble4.png'),]
        angle=math.atan2(fy,fx)
        angle=math.degrees(angle)
        self.anim2=[ pygame.transform.rotate(loadImage('assets/shots/spear1.png'),-angle),
                     pygame.transform.rotate(loadImage('assets/shots/spear2.png'),-angle),
                     pygame.transform.rotate(loadImage('assets/shots/spear3.png'),-angle),]
    def update(self):
        Shot.update(self)
        if self.timer<self.changetime and not self.changed:
            self.anim=self.anim2
            self.shape.damage*=self.multi
            self.changed=True

class BadLongShot(LongShot):
    def __init__(self,space,x,y,fx,fy,speed=120,damage=1,dt=1/120):
        LongShot.__init__(self,space,x,y,fx,fy,speed,damage,dt)
        self.shape.collision_type=collisionTypes["badshot"]
        self.multi=2

class BadSpreadShot(SpreadShot):
    def __init__(self,space,x,y,fx,fy,speed=120,damage=1,dt=1/120):
        SpreadShot.__init__(self,space,x,y,fx,fy,speed,damage,dt)
        self.shape.collision_type=collisionTypes["badshot"]

class BadSubShot(SubShot):
    def __init__(self,space,x,y,fx,fy,speed=120,damage=1,dt=1/120):
        SubShot.__init__(self,space,x,y,fx,fy,speed,damage,dt)
        self.shape.collision_type=collisionTypes["badshot"]
