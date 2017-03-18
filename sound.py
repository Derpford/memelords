import pygame, math, random
from helpers import *

pygame.mixer.pre_init(22050,-16,2,64)
pygame.mixer.init()

# Load all sounds.
sounds={"die":pygame.mixer.Sound('assets/sounds/die.ogg'),
        "die2":pygame.mixer.Sound('assets/sounds/die2.ogg'),
        "hurt":pygame.mixer.Sound('assets/sounds/hurt.ogg'),
        "shot":pygame.mixer.Sound('assets/sounds/shot.ogg'),
        "ping":pygame.mixer.Sound('assets/sounds/ping.ogg'),
        "boop":pygame.mixer.Sound('assets/sounds/boop.ogg'),
        }
# Special channels.
shotChannel=pygame.mixer.Channel(1)
hurtChannel=pygame.mixer.Channel(2)
pingChannel=pygame.mixer.Channel(3)
