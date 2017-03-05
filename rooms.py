import pygame, math, random, pytmx, pymunk
from helpers import *
from pygame.locals import *

class Room():
    def __init__(self,tile):
        self.grid=pytmx.load_pygame(tile)
        self.space=pymunk.Space()
        self.space.gravity = 0,0
        for layer in self.grid.layers:
            for x,y,img in layer.tiles():
                    props = self.grid.get_tile_properties(x,y,0)
                    if props==None:
                        pass
                    else:
                        if "solid" in props:
                            body=pymunk.Body(1,1,pymunk.Body.STATIC)
                            box=pymunk.Poly(body,[(0,0),(0,16),(16,16),(16,0)])
                            body.position=x*16,y*16
                            self.space.add(body,box)
