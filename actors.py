import pygame, math, random, pymunk
from helpers import *
debug=False

# Movement force factor.
factor=1000000
def drawAnimation(screen,frames,pos,speed,t):
    screen.blit(frames[math.floor(speed*t%len(frames))],(pos[0],pos[1]))
    if debug:
        print(str(pos)+" anim pos for "+str(math.floor(speed*t%len(frames)))+" in "+str(frames))

class Actor(pygame.sprite.Sprite):
    def __init__(self, space, x = 0, y = 0, dt = 1/120):
        self.name=None
        pygame.sprite.Sprite.__init__(self)
        self.body=pymunk.Body(1,math.inf) # Magic numbers!
        self.body.position=(x,y)
        #self.shape=pymunk.Circle(self.body,8)
        self.shape=pymunk.Circle(self.body,8)
        space.add(self.body,self.shape)
        self.rect = pygame.Rect(x,y,16,16)
        self.anim = [loadImage("assets/guy-green/guy-green1.png"),
            loadImage("assets/guy-green/guy-green2.png"),
            loadImage("assets/guy-green/guy-green3.png")]
        self.t=0
        self.dt=dt
        self.friction=150 # How hard to slow this thing down.
        self.body.jumpTo=self.jumpTo
        self.xFactor, self.yFactor= 1,1

    def jumpTo(self,pos):
        self.body.position = pos

    def draw(self,screen):
        pos=self.body.position.x+8,self.body.position.y+8
        drawAnimation(screen,self.anim,pos,8,self.t)

    def update(self):
        self.t +=self.dt
        if debug:
            if self.name:
                print(str(self.name))
            print(str(self.dx)+" dx/"+str(self.dy)+" dy")
            print(str(self.body.velocity)+" force")
            print(str(self.body.position)+" phys position")
            print(str(self.face)+" facing")
            print(str(self.t))

    def frictionUpdate(self):
        # Apply friction.
        fx = (self.body.velocity.x)*-(self.friction*self.xFactor)
        fy = (self.body.velocity.y)*-(self.friction*self.yFactor)
        self.body.apply_force_at_local_point((fx,fy),(0,0))


