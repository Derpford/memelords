import math, random, pymunk, pygame
import actors,shots
from helpers import *
from pygame.locals import *
debug=debugFlags["weapon"]

class Weapon():
    def __init__(self):
        self.damage=1
        self.maxShot=1
        self.speed=160
        self.name="Generic Weapon"
        self.anim=loadImage('assets/weapons/sword.png')
        self.face=[0,0]

    def draw(self,surf,pos,weaponAnim):
        if debugFlags["anim"]:
            print(str(math.floor(pos[0]+self.face[0]*weaponAnim*16))+","+str(math.floor(pos[1]+self.face[1]*weaponAnim*16))+" anim pos for "+str(self.anim))
            print("("+str(pos[0])+"+"+str(self.face[0])+"*"+str(weaponAnim)+"*16)")
            print("("+str(pos[1])+"+"+str(self.face[1])+"*"+str(weaponAnim)+"*16)")
        weaponPos=(pos[0]+self.face[0]*weaponAnim*16,pos[1]+self.face[1]*weaponAnim*16)
        anim=pygame.transform.flip(self.anim,self.face[0]<0,self.face[1]>0)
        surf.blit(anim,weaponPos)

    def shoot(self,space,pos,face,parent):
        # Basic shot.
        if len(parent.shotList)<self.maxShot:
            self.face=face[:]
            newShot=shots.Shot(space,pos.x+16*self.face[0],pos.y+16*self.face[1],self.face[0],self.face[1])
            parent.shotList.append(newShot)
            return True
        else: return False

class BadWeapon(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.speed=120

    def shoot(self,space,pos,face,parent):
        if len(parent.shotList)<self.maxShot:
            self.face=face[:]
            newShot=shots.BadShot(space,pos.x+16*face[0],pos.y+16*face[1],face[0],face[1])
            parent.shotList.append(newShot)
            return True
        else: return False

class Sword(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.maxShot=2




