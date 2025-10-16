import pygame
from pygame.sprite import Sprite, Group
import random

pygame.init()
screen = pygame.display.set_mode((1000, 600))
clock = pygame.time.Clock()

class Bullet(Sprite):
    def __init__(self, id, x, y):
        super().__init__()
        self.id = id
        self.image = pygame.Surface((5, 10))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()

class Enemy(Sprite):
    def __init__(self, id, x, y):
        super().__init__()
        self.id = id
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))

# Create groups
bullets = Group()
enemies = Group()

# Spawn some enemies
for id in range(22):
    enemies.add(Enemy(id, random.randint(50, 950), random.randint(50, 500)))

running = True
id = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #BB asterisk unpacks an iterable into positional arguments
            bullets.add(Bullet(id, *pygame.mouse.get_pos()))
            id += 1

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

    screen.fill((0, 0, 0))
    bullets.draw(screen)
    enemies.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
