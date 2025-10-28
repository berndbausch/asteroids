import pygame
from pygame.sprite import Sprite, Group
from pygame.math import Vector2
import random

def rotate_sprite(x, y, image, rotation):
    #BB transform.rotate() goes counter-clockwise
    rotated_img = pygame.transform.rotate(image, rotation)
    #BB correctly center the rotated image
    rotated_rect = rotated_img.get_rect(center = image.get_rect(center=(x, y)).center)
    return rotated_img, rotated_rect

screenwidth = 1000
screenheight = 600

pygame.init()
screen = pygame.display.set_mode((screenwidth, screenheight))
clock = pygame.time.Clock()

###########################################################################
class Shooter(Sprite):
    """
    BB:
    Triangle in middle of screen
    Rotates
    Shoots bullets in the direction determined by its angle
    """
###########################################################################

    def __init__(self):
        super().__init__()

        #BB Create the Surface and draw a triangle on it.
        self.xpos = screenwidth/2
        self.ypos = screenheight/2
        self.image = pygame.Surface((20, 30), pygame.SRCALPHA)
        self.orig_img = self.image
        pygame.draw.polygon(self.image, (255,255,0), [(0,30),(10,0),(20,30)])
        self.rect = self.image.get_rect(center=(self.xpos, self.ypos))

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
        self.image, self.rect = rotate_sprite(self.xpos, self.ypos, self.orig_img, self.rotation)

        #BB After rotating the triangle, also update the tip's location.
        #BB This is done using vector rotation, which goes clockwise.
        #BB Therefore, the rotation angle needs to be inversed.
        self.tipvec = self.origtipvec.rotate(-self.rotation)

###########################################################################
class Bullet(Sprite):
###########################################################################

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
        self.orig_img = self.image
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

###########################################################################
class Debris(Sprite):
    """
    A piece of a gun that explodes when it's hit by an asteroid or the enemy
    Like the gun itself, it's a triangle, though a small one
    It has a location vector, a direction vector, and a rotation with delta
    """
###########################################################################

    #BB A piece of debris is a small triangle
    #BB Both location and direction are pygame.math.Vector2 objects
    def __init__(self, id, location, direction, rotdelta):
        super().__init__()
        self.id = id
        self.location = location
        self.direction = direction

        self.rotation = 0
        self.rotdelta = rotdelta

        #BB Create the Surface and draw a triangle on it.
        self.image = pygame.Surface((5, 8), pygame.SRCALPHA)
        self.orig_img = self.image
        pygame.draw.polygon(self.image, (255,255,0), [(0,8),(2.5,0),(5,8)])
        self.rect = self.image.get_rect(center=(location))

        print(f"New debris at {self.location}, dir {self.direction}, |dir| {self.direction.length()}")

    def update(self):
        self.location = self.location+self.direction
        self.rect = self.image.get_rect(center=self.location)
        #BB rotation
        self.rotation += self.rotdelta
        self.image, self.rect = rotate_sprite(self.location.x, self.location.y, self.orig_img, self.rotation)
        #BB Dispose of the object when it reaches a border
        if self.rect.bottom < 0 or self.rect.top>screenheight or self.rect.right<0 or self.rect.left>screenwidth:
            print(f"Killing debris {self.id}")
            self.kill()

###########################################################################
class Asteroid(Sprite):
###########################################################################

    def __init__(self, id, x, y, angle=45, speed=5):
        super().__init__()
        self.id = id
        self.location = Vector2(x, y)
        self.direction = Vector2(0, speed).rotate(angle)

        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=self.location)

        print(f"asteroid {self.id}, loc {self.location}, dir {self.direction}")

    def update(self):
        self.location = self.location+self.direction
        self.rect = self.image.get_rect(center=self.location)
        #if self.id==0:
            #print(f"new loc {self.location}, left {self.rect.left}, right {self.rect.right}, top {self.rect.top}, bottom {self.rect.bottom}")
        #BB Wrap around when object reaches a border
        if self.rect.bottom < 0:
            self.rect.top = screenheight
            self.location.update(self.rect.center)
        elif self.rect.top>screenheight:
            self.rect.bottom = 0
            self.location.update(self.rect.center)
        elif self.rect.right<0:
            self.rect.left = screenwidth
            self.location.update(self.rect.center)
        elif self.rect.left>screenwidth:
            self.rect.right = 0
            self.location.update(self.rect.center)

# Create groups
gungroup = Group()
bullets = Group()
asteroids = Group()
debris = Group()

#BB Create the gun
gun = Shooter()
gungroup.add(gun)

# Create some asteroids
#BB Ensure they are not too close to the gun in the center of the screen
for id in range(22):
    if random.choice([True,False]):
        x = random.randint(0, screenwidth/4)
    else:
        x = random.randint(3*screenwidth/3, screenwidth)
    if random.choice([True,False]):
        y = random.randint(0, screenheight/4)
    else:
        y = random.randint(3*screenheight/3, screenheight)
    
    angle = random.randint(0, 360)
    speed = random.uniform(0.1, 2)
    asteroids.add(Asteroid(id, x, y, angle, speed))

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
        asteroids.update()
        gungroup.update()
        bullets.update()
        debris.update()

        # Detect collisions
        #BB groupcollide(group1, group2, dokill1, dokill2, collided = None)
        #BB The dokill parameters determine if collided elements are removed
        #BB Returns dictionary of all detected collisions.
        #BB Key is a bullet, value is a list of asteroids.
        #BB If no collision occurs, returns an empty dict.
        #BB
        #BB Here, we check collisions between all bullets and all asteroids.
        #BB Asteroids that collide with bullets will be removed.
        collision = pygame.sprite.groupcollide(bullets, asteroids, False, True)
        if len(collision)>0:
            for coll in collision:
                print(coll.id, end=": ")
                for asteroid in collision[coll]:
                    print(asteroid.id, end=",")
            print()

        #BB Next, we check if the gun collides with an asteroid.
        #BB If yes, the gun disappears and the game is over.
        #BB In the future, the gun explodes and the asteroid breaks up.
        collision = pygame.sprite.groupcollide(gungroup, asteroids, True, False)
        if len(collision)>0:
            for id in range(10):
                speed = random.uniform(0.1, 2)
                d = Debris(id, gun.imgvec, Vector2(0, speed).rotate(id*36), random.uniform(0.1,6))
                debris.add(d)

    #BB display all objects on the screen
    screen.fill((100, 100, 100))
    bullets.draw(screen)
    asteroids.draw(screen)
    gungroup.draw(screen)
    debris.draw(screen)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
