import pygame, math, random, pymunk
from helpers import *
import actors,weapons
debug=debugFlags["player"]

class Player(actors.Actor):
    def __init__(self,space, x=0, y=0, dt=1/120):
        actors.Actor.__init__(self,space,x,y,dt)
        self.shape=pymunk.Circle(self.body,8)
        self.shape.newRoomFlag=False
        space.add(self.body,self.shape)
        self.shape.collision_type = collisionTypes["player"]
        self.anim = [loadImage("assets/guy-green/guy-green1.png"),
                loadImage("assets/guy-green/guy-green2.png"),
                loadImage("assets/guy-green/guy-green3.png"),
                loadImage("assets/guy-green/guy-green4.png"),
                loadImage("assets/guy-green/guy-green5.png"),
                loadImage("assets/guy-green/guy-green6.png"),
                pygame.transform.flip(loadImage("assets/guy-green/guy-green4.png"),True,False),
                pygame.transform.flip(loadImage("assets/guy-green/guy-green5.png"),True,False),
                pygame.transform.flip(loadImage("assets/guy-green/guy-green6.png"),True,False),
                loadImage("assets/guy-green/guy-green7.png"),
                loadImage("assets/guy-green/guy-green8.png"),
                loadImage("assets/guy-green/guy-green9.png")]
        self.face=[0,1]
        self.speed=120
        self.dx=0
        self.dy=0
        self.hp=6
        self.maxhp=6
        self.dead=False
        self.shotList=[]
        self.weapon=weapons.Sword()
        self.weaponAnim=0

    def draw(self,screen):
        pos=(self.body.position.x-8,self.body.position.y-8)
        # Draw weapon.
        if self.weaponAnim>0.2:
            self.weaponAnim-=self.dt*4
            self.weapon.draw(screen,pos,self.weaponAnim)

        if self.keys[pygame.K_LEFT] or self.keys[pygame.K_RIGHT] or self.keys[pygame.K_UP] or self.keys[pygame.K_DOWN]:
            # Walking.
            if self.face[0]!=0:
                if self.face[0]>0:
                    actors.drawAnimation(screen,self.anim[4:6],pos,8*abs(self.face[0]),self.t)
                if self.face[0]<0:
                    actors.drawAnimation(screen,self.anim[7:9],pos,8*abs(self.face[0]),self.t)
            else:
                if self.face[1]<0:
                    actors.drawAnimation(screen,self.anim[10:12],pos,8*abs(self.face[1]),self.t)
                else:
                    actors.drawAnimation(screen,self.anim[1:3],pos,8*abs(self.face[1]),self.t)
        else:
            # Standing.
            if self.face[0]!=0:
                if self.face[0]>0:
                        screen.blit(self.anim[3],pos)
                if self.face[0]<0:
                        screen.blit(self.anim[6],pos)
            else:
                if self.face[1]<0:
                    screen.blit(self.anim[9],pos)
                else:
                    screen.blit(self.anim[0],pos)


        # Draw shots.
        for shot in self.shotList:
            shot.draw(screen)

    def hurt(self,amount):
        self.hp-=amount
        if self.hp <= 0:
            self.dead=True
    def heal(self,amount):
        self.hp=min(self.maxhp, self.hp+amount)
        if self.dead:
            self.dead=False

    def physicsUpdate(self):
            self.xFactor=1
            self.yFactor=1
            # Adjust friction for moving the other way.
            if self.body.velocity.x !=0:
                if self.face[0]!=normal(self.body.velocity.x):
                    self.xFactor*=2
                    self.face[0]*=2
            if self.body.velocity.y !=0:
                if self.face[1]!=normal(self.body.velocity.y):
                    self.yFactor*=2
                    self.face[1]*=2
            if self.keys[pygame.K_LEFT] or self.keys[pygame.K_RIGHT] or self.keys[pygame.K_UP] or self.keys[pygame.K_DOWN]:
                # Reset facing at the beginning of each frame that we walk.
                self.face[0]=0
                self.face[1]=0
                # Set new facing.
                if self.keys[pygame.K_LEFT]:
                    self.face[0]=-1
                if self.keys[pygame.K_RIGHT]:
                    self.face[0]=1
                if self.keys[pygame.K_UP]:
                    self.face[1]=-1
                if self.keys[pygame.K_DOWN]:
                    self.face[1]=1
                # Apply new movement.
                angle=math.atan2(self.face[1],self.face[0])
                self.dx=math.cos(angle)*self.speed*self.dt*self.xFactor
                self.dy=math.sin(angle)*self.speed*self.dt*self.yFactor
                # Apply force.
                self.body.apply_force_at_local_point((self.dx*actors.factor,self.dy*actors.factor),(0,0))

            # Friction.
            self.frictionUpdate()


        
    def update(self,mapGrid):
        actors.Actor.update(self)
        if self.shape.newRoomFlag:
            for shot in self.shotList:
                mapGrid.space.remove(shot.body, shot.shape)
            self.shotList=[]
            self.shape.newRoomFlag=False
        if not self.dead:
            self.keys=pygame.key.get_pressed()
            self.physicsUpdate()
            for shot in self.shotList:
                shot.update()
                if debug:
                    print("Handling shot, removeFlag: "+str(shot.shape.removeFlag))
                    print("shot position: "+str(shot.body.position))
                if shot.shape.removeFlag == True:
                    mapGrid.space.remove(shot.body)
                    mapGrid.space.remove(shot.shape)
            self.shotList=[shot for shot in self.shotList if shot.shape.removeFlag==False]
            if self.keys[pygame.K_LCTRL] and self.weaponAnim<=0.5:
                newShot=self.weapon.shoot(mapGrid.space,self.body.position,self.face,self)
                if newShot:self.weaponAnim=1

