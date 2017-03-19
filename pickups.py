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
        if debugFlags["actor"] or debugFlags["pickup"]:
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
        if debugFlags["actor"] or debugFlags["pickup"]:
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
        self.shape.weaponType=weapons.Weapon

    def pickup(self,other):
        if debugFlags["actor"] or debugFlags["pickup"]:
            print("Weapon grabbed, "+str(self.shape.weaponType))
        if isinstance(other.getWeapon(),weapons.Weapon):
            if other.getWeapon().name==self.shape.weaponType.name:
                if debugFlags["pickup"]:
                    print("Same type, power up 1")
                other.getWeapon().powerUp(1)
            else:
                if debugFlags["pickup"]:
                    print("Different type, switch weapon")
                other.setWeapon(self.shape.weaponType)

class SwordPickup(WeaponPickup):
    def __init__(self,space,x=0,y=0,dt=1/120):
        WeaponPickup.__init__(self,space,x,y,dt)
        self.shape.weaponType=weapons.Sword
        self.anim=[loadImage('assets/weapons/sword.png')]

class SpearPickup(WeaponPickup):
    def __init__(self,space,x=0,y=0,dt=1/120):
        WeaponPickup.__init__(self,space,x,y,dt)
        self.shape.weaponType=weapons.Spear
        self.anim=[loadImage('assets/weapons/spear.png')]

class AxePickup(WeaponPickup):
    def __init__(self,space,x=0,y=0,dt=1/120):
        WeaponPickup.__init__(self,space,x,y,dt)
        self.shape.weaponType=weapons.Axe
        self.anim=[loadImage('assets/weapons/axe.png')]

