from helpers import *


hudSurface=None
barSprites=None
heartSprites=None

# Hud surface and sprites.
def hudInit():
    global heartSprites, barSprites, hudSurface
    heartSprites = [loadImage('assets/hud/heart1.png'),loadImage('assets/hud/heart2.png'),loadImage('assets/hud/heart2.png')]
    barSprites =[loadImage('assets/hud/bar1.png'),loadImage('assets/hud/bar2.png')] 
    hudSurface = pygame.Surface((400,96))
    hudSprites = loadImage('assets/hud/bg.png')
    hudTopSprite = pygame.Surface((384,8))
    hudBottomSprite = pygame.Surface((384,8))
    hudLeftSprite = pygame.Surface((8,80))
    hudRightSprite = pygame.Surface((8,80))
    hudSurface.fill((133,149,80))
    hudSurface.blit(hudSprites,(0,0),pygame.Rect(0,0,8,8))
    hudSurface.blit(hudSprites,(392,0),pygame.Rect(24,0,8,8))
    hudSurface.blit(hudSprites,(0,88),pygame.Rect(0,24,8,8))
    hudSurface.blit(hudSprites,(392,88),pygame.Rect(24,24,8,8))
    
    # Top, Bottom, Left and Right sides
    for i in range(0,math.floor(384/16)):
        hudTopSprite.blit(hudSprites,(i*16,0),pygame.Rect(8,0,16,8))
    for i in range(0,math.floor(384/16)):
        hudBottomSprite.blit(hudSprites,(i*16,0),pygame.Rect(8,24,16,8))
    for i in range(0,math.floor(80/16)):
        hudLeftSprite.blit(hudSprites,(0,i*16),pygame.Rect(0,8,8,16))
    for i in range(0,math.floor(80/16)):
        hudRightSprite.blit(hudSprites,(0,i*16),pygame.Rect(24,8,8,16))
    hudSurface.blit(hudTopSprite,(8,0))
    hudSurface.blit(hudBottomSprite,(8,88))
    hudSurface.blit(hudLeftSprite,(0,8))
    hudSurface.blit(hudRightSprite,(392,8))
    hpBlit=gameFont.render("Health",False,textColors["dark"])
    weaponBlit=gameFont.render("Weapon",False,textColors["dark"])
    hudSurface.blit(hpBlit,(16,12))
    hudSurface.blit(weaponBlit,(16,48))
    return hudSurface

def drawHud(screen,surf,pos,player):
    screen.blit(surf,pos)
    for i in range(0,player.maxhp):
        if i >= player.hp:
            screen.blit(barSprites[1],tupSum(pos,(16+i*4,24)))
        else:
            screen.blit(barSprites[0],tupSum(pos,(16+i*4,24)))
