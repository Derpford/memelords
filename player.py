import pygame, math, random, pymunk
from helpers import *
import actors
debug=False

class Player(actors.Actor):
    def __init__(self,space, x=0, y=0, dt=1/120):
        actors.Actor.__init__(self,space,x,y,dt)
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


    def draw(self,screen):
        pos=(self.body.position.x-8,self.body.position.y-8)
        if pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_DOWN]:
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

    def hurt(self,amount):
        self.hp-=amount
        if self.hp <= 0:
            self.dead=True
    def heal(self,amount):
        self.hp=min(self.maxhp, self.hp+amount)
        if self.dead:
            self.dead=False

        
    def update(self,mapGrid):
        frict=self.friction
        self.t+=self.dt
        if not self.dead:
            xFactor=1
            yFactor=1
            if pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_DOWN]:
                # Reset facing at the beginning of each frame that we walk.
                self.face[0]=0
                self.face[1]=0
                # Set new facing.
                if pygame.key.get_pressed()[pygame.K_LEFT]:
                    self.face[0]=-1
                if pygame.key.get_pressed()[pygame.K_RIGHT]:
                    self.face[0]=1
                if pygame.key.get_pressed()[pygame.K_UP]:
                    self.face[1]=-1
                if pygame.key.get_pressed()[pygame.K_DOWN]:
                    self.face[1]=1
                # Adjust friction for moving the other way.
                if self.body.velocity.x !=0:
                    if self.face[0]!=self.body.velocity.x/abs(self.body.velocity.x):
                        xFactor*=2
                        self.face[0]*=2
                if self.body.velocity.y !=0:
                    if self.face[1]!=self.body.velocity.y/abs(self.body.velocity.y):
                        yFactor*=2
                        self.face[1]*=2
                # Apply new movement.
                angle=math.atan2(self.face[1],self.face[0])
                self.dx=math.cos(angle)*self.speed*self.dt*xFactor
                self.dy=math.sin(angle)*self.speed*self.dt*yFactor
                # Apply force.
                self.body.apply_force_at_local_point((self.dx*actors.factor,self.dy*actors.factor),(0,0))
            # Apply friction.
            fx = (self.body.velocity.x)*-(frict*xFactor)
            fy = (self.body.velocity.y)*-(frict*yFactor)
            self.body.apply_force_at_local_point((fx,fy),(0,0))
            if debug:
                print(str(self.dx)+" dx/"+str(self.dy)+" dy")
                print(str(self.body.velocity)+" force")
                print(str(self.body.position)+" phys position")

            # Handle exiting rooms.
            
