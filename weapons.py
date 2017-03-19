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
        self.shot=shots.Shot

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
            newShot=self.shot(space,pos.x+16*self.face[0],pos.y+16*self.face[1],self.face[0],self.face[1])
            parent.shotList.append(newShot)
            return True
        else: return False

class BadWeapon(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.speed=120
        self.shot=shots.BadShot

class Sword(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.maxShot=2

class Spear(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.maxShot=1
        self.shot=shots.LongShot
        self.anim=loadImage('assets/weapons/spear.png')

class Axe(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.name="Axe"
        self.maxShot=1
        self.anim=loadImage('assets/weapons/axe.png')
        self.shot=shots.SpreadShot
        self.shot2=shots.SubShot

    def shoot(self,space,pos,face,parent):
        # Spread shot.
        if len(parent.shotList)<self.maxShot:
            self.face=face[:]
            angle=math.atan2(self.face[1],self.face[0])
            angleL=angle+math.pi*0.125
            angleR=angle-math.pi*0.125
            faceLeft=math.cos(angleL),math.sin(angleL)
            faceRight=math.cos(angleR),math.sin(angleR)
            newShot=self.shot(space,pos.x+16*self.face[0],pos.y+16*self.face[1],self.face[0],self.face[1])
            parent.shotList.append(newShot)
            spreadShot=self.shot2(space,pos.x+16*self.face[0],pos.y+16*self.face[1],faceLeft[0],faceLeft[1])
            parent.shotList.append(spreadShot)
            spreadShot=self.shot2(space,pos.x+16*self.face[0],pos.y+16*self.face[1],faceRight[0],faceRight[1])
            parent.shotList.append(spreadShot)
            return True
        else: return False

    def draw(self,surf,pos,weaponAnim):
        if debugFlags["anim"]:
            print(str(math.floor(pos[0]+self.face[0]*weaponAnim*16))+","+str(math.floor(pos[1]+self.face[1]*weaponAnim*16))+" anim pos for "+str(self.anim))
            print("("+str(pos[0])+"+"+str(self.face[0])+"*"+str(weaponAnim)+"*16)")
            print("("+str(pos[1])+"+"+str(self.face[1])+"*"+str(weaponAnim)+"*16)")
        weaponPos=(pos[0]+self.face[0]*weaponAnim*16,pos[1]+self.face[1]*weaponAnim*16)
        anim=pygame.transform.flip(self.anim,self.face[0]<0,False)
        surf.blit(anim,weaponPos)

class BadAxe(Axe):
    def __init__(self):
        Axe.__init__(self)

    def shoot(self,space,pos,face,parent):
        # Spread shot.
        if len(parent.shotList)<self.maxShot:
            self.face=face[:]
            angle=math.atan2(self.face[1],self.face[0])
            angleL=angle+math.pi*0.125
            angleR=angle-math.pi*0.125
            faceLeft=math.cos(angleL),math.sin(angleL)
            faceRight=math.cos(angleR),math.sin(angleR)
            newShot=shots.BadSpreadShot(space,pos.x+16*self.face[0],pos.y+16*self.face[1],self.face[0],self.face[1])
            parent.shotList.append(newShot)
            spreadShot=shots.BadSubShot(space,pos.x+16*self.face[0],pos.y+16*self.face[1],faceLeft[0],faceLeft[1])
            parent.shotList.append(spreadShot)
            spreadShot=shots.BadSubShot(space,pos.x+16*self.face[0],pos.y+16*self.face[1],faceRight[0],faceRight[1])
            parent.shotList.append(spreadShot)
            return True
        else: return False
