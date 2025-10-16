import pygame
from pygame.sprite import Sprite
from pygame.math import Vector2
import random

screenwidth, screenheight = 1000, 600

pygame.init()
screen = pygame.display.set_mode((screenwidth, screenheight))
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
        #BB We start with a Surface, on which we draw a triangle
        self.image = pygame.Surface((w, h))
        self.origimg = self.image
        pygame.draw.polygon(self.image, (255,255,0), [(0,h),(w/2,0),(w,h)], 3)

        #BB get the Rect for this Surface
        #BB it contains the display coordinates of the Surface
        self.rect = self.image.get_rect(center=(x, y))

        #BB the vector to the image center is needed to calculate rotation
        self.imgvec = Vector2(self.rect.center)

        #BB New Surface to visualize the tip of the gun
        self.tip = pygame.Surface((10,10))
        self.tip.fill((255,0,0))

        #BB The tip's vector relative to the Surface center
        self.tipvec = Vector2(self.rect.midtop) - self.imgvec
        self.origtipvec = self.tipvec

        #BB Adding the Surface center's vector and the tip vector
        #BB results in the tip's location
        self.tiprect = self.tip.get_rect(center=self.imgvec+self.tipvec)

        self.rotation = 0
        self.rotdelta = 0

    def update(self):
        self.rotation += self.rotdelta

        #BB rotate the shooter itself
        #BB transform.rotate() goes counter-clockwise
        rotimg = pygame.transform.rotate(self.origimg, self.rotation)
        #BB correctly center the rotated image
        rotrect = rotimg.get_rect(center=self.origimg.get_rect(center=(screenwidth/2, screenheight/2)).center)
        self.image = rotimg
        self.rect = rotrect

        #BB after rotating the triangle, also update the tip's location
        #BB this is done using vector rotation, which goes clockwise
        #BB therefore, the rotation angle needs to be inversed
        self.tipvec = self.origtipvec.rotate(-self.rotation)
        #BB the tip's location is calculated by adding the image vector
        #BB and the tip vector
        self.tiprect = self.tip.get_rect(center=self.imgvec+self.tipvec)

v1 = Vector2(screenwidth/2, screenheight/2)
s1 = Shooter(*v1, 70, 70)

running = True
while running:
    for ev in pygame.event.get():
        if ev.type==pygame.KEYDOWN:
            if ev.key==pygame.K_a:
                s1.rotdelta = 3
            if ev.key==pygame.K_s:
                s1.rotdelta = -3
            if ev.key==pygame.K_x:
                print("Bye!")
                running = False
        if ev.type==pygame.KEYUP:
            if ev.key==pygame.K_a or ev.key==pygame.K_s:
                s1.rotdelta = 0

    s1.update()
    screen.fill((0, 0, 0))
    #BB copy the triangle and the tip onto the screen Surface
    screen.blit(s1.image, s1.rect)
    screen.blit(s1.tip, s1.tiprect)

    #BB display the drawing buffer
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
