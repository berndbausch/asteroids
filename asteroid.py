import pygame
from pygame.sprite import Sprite, Group
from pygame.math import Vector2
import random

screenwidth = 1000
screenheight = 600

pygame.init()
screen = pygame.display.set_mode((screenwidth, screenheight))
clock = pygame.time.Clock()

class Shooter(Sprite):
    """
    BB:
    Triangle in middle of screen
    Rotates
    Shoots bullets in the direction determined by its angle
    """

    def __init__(self):
        super().__init__()

        #BB Create the Surface and draw a triangle on it.
        self.image = pygame.Surface((20, 30))
        self.original = self.image
        pygame.draw.polygon(self.image, (255,255,0), [(0,30),(10,0),(20,30)])
        self.rect = self.image.get_rect(center=(screenwidth/2, screenheight/2))

        #BB Vector of shooter's center
        self.imgvec = Vector2(self.rect.center)

        #BB tipvec is the vector to the tip of the gun, relative to imgvec
        self.tipvec = Vector2(self.rect.midtop) - self.imgvec
        self.origtipvec = self.tipvec

        self.rotation = 0  #BB degrees
        self.rotdelta = 0

    #BB Rotate and move the triangle
    def update(self):
        self.rotation += self.rotdelta

        #BB rotate the shooter itself
        #BB transform.rotate() goes counter-clockwise
        rotated_img = pygame.transform.rotate(self.original, self.rotation)
        #BB correctly center the rotated image
        rotated_rect = rotated_img.get_rect(center = self.original.get_rect(center=(screenwidth/2, screenheight/2)).center)
        self.image = rotated_img
        self.rect = rotated_rect

        #BB after rotating the triangle, also update the tip's location
        #BB this is done using vector rotation, which goes clockwise
        #BB therefore, the rotation angle needs to be inversed
        self.tipvec = self.origtipvec.rotate(-self.rotation)

class Bullet(Sprite):

    #BB Both location and direction are pygame.math.Vector2 objects
    #BB Size is bullet's diameter
    def __init__(self, id, location, direction, size=5):
        super().__init__()
        self.id = id
        self.location = location
        self.direction = direction.normalize()
        self.direction.scale_to_length(8)   #BB length determines speed

        #BB Create Surface and draw circle on it
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(center=location)
        pygame.draw.circle(self.image, (255,255,0), (size/2,size/2), size/2)

        print(f"New bullet at {self.location}, dir {self.direction}, |dir| {self.direction.length()}")

    def update(self):
        self.location = self.location+self.direction
        self.rect = self.image.get_rect(center=self.location)
        #BB Dispose of the object when it reaches a border
        if self.rect.bottom < 0 or self.rect.top>screenheight or self.rect.right<0 or self.rect.left>screenwidth:
            print(f"Killing bullet {self.id}")
            self.kill()

class Enemy(Sprite):
    def __init__(self, id, x, y):
        super().__init__()
        self.id = id
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))

# Create groups
gungroup = Group()
bullets = Group()
enemies = Group()

#BB Create the gun
gun = Shooter()
gungroup.add(gun)

# Spawn some enemies
for id in range(22):
    enemies.add(Enemy(id, random.randint(50, 950), random.randint(50, 500)))

running = True
pausing = False
id = 0
while running:
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                running = False
            case pygame.MOUSEBUTTONDOWN:
                #BB asterisk unpacks an iterable into positional arguments
                #BB bullets.add(Bullet(id, *pygame.mouse.get_pos()))
                #BB id += 1
                pass
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_SPACE:
                        bullets.add(Bullet(id, gun.imgvec+gun.tipvec, gun.tipvec))
                        print(f"Shooting from {gun.imgvec+gun.tipvec}")
                        id += 1
                    case pygame.K_a:    #BB counter-clockwise
                        gun.rotdelta = 3 
                    case pygame.K_s:    #BB clockwise
                        gun.rotdelta = -3 
                    case pygame.K_x: 
                        running = False
                    case pygame.K_p:
                        pausing = not pausing
                        if pausing:
                            print("pausing")
                        else:
                            print("resuming")
            case pygame.KEYUP:
                if event.key==pygame.K_a or event.key==pygame.K_s:
                    gun.rotdelta = 0

    if not pausing:
        gungroup.update()
        bullets.update()

        # Detect collisions
        #BB groupcollide(group1, group2, dokill1, dokill2, collided = None)
        #BB The dokill parameters determine if collided elements are removed
        #BB Returns dictionary of all detected collisions.
        #BB Key is a bullet, value is a list of enemies.
        #BB If no collision occurs, returns an empty dict.
        collision = pygame.sprite.groupcollide(bullets, enemies, False, True)
        if len(collision)>0:
            for coll in collision:
                print(coll.id, end=": ")
                for enemy in collision[coll]:
                    print(enemy.id, end=",")
            print()

    #BB display all objects on the screen
    screen.fill((0, 0, 0))
    gungroup.draw(screen)
    bullets.draw(screen)
    enemies.draw(screen)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
