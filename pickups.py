import math, random, types, pymunk
import actors,sound,weapons
from helpers import *
from pygame.locals import *
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

class Money(Pickup):
    def __init__(self, space, x = 0, y = 0, dt = 1/120):
        Pickup.__init__(self,space,x,y,dt)
        self.anim=[loadImage('assets/sapir1.png'),loadImage('assets/sapir2.png')]
    
    def pickup(self,other):
        if debugFlags["actor"]:
            print("Pickup grabbed")
        if type(other.addMoney)==types.MethodType:
            other.addMoney(1)

    def draw(self,screen):
        pos=self.body.position.x-4,self.body.position.y-4
        actors.drawAnimation(screen,self.anim,pos,16,self.t)

class WeaponPickup(Pickup):
    def __init__(self,space,x=0,y=0,dt=1/120):
        Pickup.__init__(self,space,x,y,dt)
        self.anim=[loadImage('assets/rice.png')]
        self.weaponType=weapons.Weapon

    def pickup(self,other):
        if debugFlags["actor"]:
            print("Weapon grabbed")
        if other.weapon is weapons.Weapon:
            if other.weapon is self.weaponType:
                other.weapon.damage+=1
            else:
                other.weapon=self.weaponType()

class SwordPickup(WeaponPickup):
    def __init__(self,space,x=0,y=0,dt=1/120):
        WeaponPickup.__init(self,space,x,y,dt)
        self.weaponType=weapons.Sword
        self.anim=[loadImage('assets/weapons/sword.png')]

class SpearPickup(WeaponPickup):
    def __init__(self,space,x=0,y=0,dt=1/120):
        WeaponPickup.__init(self,space,x,y,dt)
        self.weaponType=weapons.Spear
        self.anim=[loadImage('assets/weapons/spear.png')]

class AxePickup(WeaponPickup):
    def __init__(self,space,x=0,y=0,dt=1/120):
        WeaponPickup.__init(self,space,x,y,dt)
        self.weaponType=weapons.Axe
        self.anim=[loadImage('assets/weapons/axe.png')]

