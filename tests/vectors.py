import pygame
from pygame.sprite import Sprite
from pygame.math import Vector2
import random

pygame.init()
screen = pygame.display.set_mode((1000, 600))
clock = pygame.time.Clock()

class Shooter(Sprite):
    """
    image
    rect
    rotation
    rotdelta
    """
    def __init__(self, x, y, w=100, h=100):
        super().__init__()

        #BB For convenience, remember the coordinates
        self.w = w
        self.h = h
        self.x = x
        self.y = y

        #BB Create and draw a rudimentary gun
        self.image = pygame.Surface((w, h))
        self.origimg = self.image
        self.image.fill((255, 255, 0))
        pygame.draw.polygon(self.image, (0,0,0), [(0,h),(w/2,0),(w,h)], 3)

        #BB get the Rect for this Surface
        #BB it contains the display coordinates of the Surface
        self.rect = self.image.get_rect(center=(x, y))
        self.imgvec = Vector2(self.rect.center)

        #BB New Surface to indicate the tip of the gun
        self.tip = pygame.Surface((10,10))
        self.tip.fill((255,0,0))
        self.tipvec = Vector2(self.rect.midtop) - self.imgvec
        self.tiprect = self.tip.get_rect(center=self.imgvec+self.tipvec)

        self.rotation = 0
        self.rotdelta = 0

    def update(self):
        self.rotation += self.rotdelta
        rotimg = pygame.transform.rotate(self.origimg, self.rotation)
        rotrect = rotimg.get_rect(center=self.origimg.get_rect(center=(screenwidth/2, screenheight/2)).center)

v1 = Vector2(500, 300)
s1 = Shooter(*v1, 70, 70)
s2 = None
rotation = 0

while True:
    for ev in pygame.event.get():
        if ev.type==pygame.KEYDOWN:
            if ev.key==pygame.K_a:
                rotdelta = 3
            if ev.key==pygame.K_s:
                rotdelta = -3
            rotation += rotdelta
            v2 = v1.rotate(rotation)
            s2 = Shooter(*v2, 50, 50)

            print(f"v1 {v1}, v2 {v2}")

    screen.fill((0, 0, 0))
    screen.blit(s1.image, s1.rect)
    screen.blit(s1.tip, s1.tiprect)
    if (s2!=None):
        screen.blit(s2.image, s2.rect)
        screen.blit(s2.tip, s2.tiprect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
