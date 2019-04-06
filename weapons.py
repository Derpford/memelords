import math, random, pymunk, pygame
import actors,shots
from helpers import *
from pygame.locals import *
debug=debugFlags["weapon"]

class Weapon():
    name="Generic Weapon"
    def __init__(self):
        self.damage=1
        self.power=3
        self.charge=192
        self.maxCharge=192
        self.maxShot=1
        self.speed=160
        self.anim=loadImage('assets/weapons/sword.png')
        self.face=[0,0]
        self.shot=shots.Shot
        self.room = None

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
        if debug:print("Shot "+str(self.shot)+" with damage "+str(self.damage))
        if len(parent.shotList)<self.maxShot:
            self.face=face[:]
            newShot=self.shot(space,pos.x+16*self.face[0],pos.y+16*self.face[1],self.face[0],self.face[1],damage=self.damage)
            newShot.room = parent.room
            newShot.shape.room = parent.room
            parent.shotList.append(newShot)
            if self.charge > 0:
                self.charge -=1
                self.power = math.ceil(self.charge/self.maxCharge*3)
            return True
        else: return False

    def powerUp(self,amt):
        self.power+=amt
        if debug:print("Powered up "+str(amt)+", new damage "+str(self.damage))

class BadWeapon(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.power=1
        self.charge=0
        self.speed=120
        self.shot=shots.BadShot

class BadWeaponRapid(BadWeapon):
    def __init__(self):
        BadWeapon.__init__(self)
        self.maxShot=2
        self.shot=shots.BadSubShot


class Sword(Weapon):
    name="Sword"
    def __init__(self):
        Weapon.__init__(self)
        self.maxShot=2

    def shoot(self,space,pos,face,parent):
        self.maxShot=self.power+1
        return Weapon.shoot(self,space,pos,face,parent)

class Spear(Weapon):
    name="Spear"
    def __init__(self):
        Weapon.__init__(self)
        self.maxShot=1
        self.power=3
        self.shot=shots.LongShot
        self.anim=loadImage('assets/weapons/spear.png')

    def shoot(self,space,pos,face,parent):
        if debug:print("Shot "+str(self.shot)+" with damage "+str(self.damage))
        if len(parent.shotList)<self.maxShot:
            self.face=face[:]
            newShot=self.shot(space,pos.x+16*self.face[0],pos.y+16*self.face[1],self.face[0],self.face[1],
                    damage=self.damage,multi=self.power+1)
            newShot.room = parent.room
            newShot.shape.room = parent.room
            parent.shotList.append(newShot)
            if self.charge > 0:
                self.charge -=1
                self.power = math.ceil(self.charge/self.maxCharge*3)
            return True
        else: return False

class BadSpear(Spear):
    name="BadSpear"
    def __init__(self):
        Weapon.__init__(self)
        self.power=1
        self.shot=shots.BadLongShot
    def shoot(self,space,pos,face,parent):
        return Weapon.shoot(self,space,pos,face,parent)

class Axe(Weapon):
    name="Axe"
    def __init__(self):
        Weapon.__init__(self)
        self.name="Axe"
        self.maxShot=1
        self.charge=96
        self.maxCharge=96
        self.power=3
        self.anim=loadImage('assets/weapons/axe.png')
        self.shot=shots.SpreadShot
        self.shot2=shots.SubShot

    def shoot(self,space,pos,face,parent):
        # Spread shot.
        self.damage=self.power
        if len(parent.shotList)<self.maxShot:
            self.face=face[:]
            # Get a pair of angles for the split shots.
            angle=math.atan2(self.face[1],self.face[0])
            angleL=angle+math.pi*0.125
            angleR=angle-math.pi*0.125
            faceLeft=math.cos(angleL),math.sin(angleL)
            faceRight=math.cos(angleR),math.sin(angleR)
            # Main shot.
            newShot=self.shot(space,pos.x+16*self.face[0],pos.y+16*self.face[1],self.face[0],self.face[1],damage=self.damage)
            newShot.room = parent.room
            newShot.shape.room = parent.room
            parent.shotList.append(newShot)
            # Subshots.
            spreadShot=self.shot2(space,pos.x+16*self.face[0],pos.y+16*self.face[1],faceLeft[0],faceLeft[1],damage=1)
            spreadShot.room = parent.room
            spreadShot.shape.room = parent.room
            parent.shotList.append(spreadShot)
            spreadShot=self.shot2(space,pos.x+16*self.face[0],pos.y+16*self.face[1],faceRight[0],faceRight[1],damage=1)
            spreadShot.room = parent.room
            spreadShot.shape.room = parent.room
            parent.shotList.append(spreadShot)
            if self.charge > 0:
                self.charge -=1
                self.power = math.ceil(self.charge/self.maxCharge*3)
            return True
        else: return False

    # Custom render code because the axe looks weird otherwise.
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
        self.power=1
        self.shot=shots.BadSpreadShot
        self.shot2=shots.BadSubShot

class Dagger(Weapon):
    name="Dagger"
    def __init__(self):
        Weapon.__init__(self)
        self.name="Dagger"
        self.maxShot=1
        self.charge=96
        self.maxCharge=96
        self.power=3
        self.anim=loadImage('assets/weapons/twindagger.png')
        self.shot=shots.SubShot

    def shoot(self,space,pos,face,parent):
        # Spread shot.
        self.damage=self.power
        if len(parent.shotList)<self.maxShot:
            self.face=face[:]
            for i in range(0,self.power):
                # Get a pair of angles for the split shots.
                angle=math.atan2(self.face[1],self.face[0])
                angleL=angle+math.pi*0.125*i+0.5#random.randrange(1,self.power+1)
                angleR=angle-math.pi*0.125*i-0.5#random.randrange(1,self.power+1)
                faceLeft=math.cos(angleL),math.sin(angleL)
                faceRight=math.cos(angleR),math.sin(angleR)
                # Subshots.
                spreadShotLeft=self.shot(space,pos.x+16*self.face[0],pos.y+16*self.face[1],faceLeft[0],faceLeft[1],damage=1)
                spreadShotLeft.room = parent.room
                spreadShotLeft.shape.room = parent.room
                parent.shotList.append(spreadShotLeft)
                spreadShotRight=self.shot(space,pos.x+16*self.face[0],pos.y+16*self.face[1],faceRight[0],faceRight[1],damage=1)
                spreadShotRight.room = parent.room
                spreadShotRight.shape.room = parent.room
                parent.shotList.append(spreadShotRight)
            if self.charge > 0:
                self.charge -=1
                self.power = math.ceil(self.charge/self.maxCharge*3)
            return True
        else: return False

