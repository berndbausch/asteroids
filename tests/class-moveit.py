import pygame
import random
import sys
from gameobject import GameObject 

screenwidth = 800
screenheight = 800
black = 0, 0, 0   # background colour

def moveball(ball, image):
    ball.move()
    if ball.pos.right>=screenwidth or ball.pos.left<=0:
        ball.speedx = -ball.speedx
    if ball.pos.bottom>=screenheight or ball.pos.top<=0:
        ball.speedy = -ball.speedy
    screen.blit(image, ball.pos)

maxspeed = 10
def adjust_speed(speed, delta):
    # don't go above maxspeed
    if abs(speed)==maxspeed and delta>0:
        return speed

    return speed+delta

screen = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()

background = pygame.image.load('background.jpg').convert()
screen.blit(background, (0, 0))
# screen.fill(black)
pygame.display.update()

# Create several automatically moving ball objects
ballimg = pygame.image.load('ball.gif').convert_alpha()
balls = []
for i in range(6):
    spx = random.randrange(1,3,1)
    spy = random.randrange(1,4,1)
    starty = random.randrange(screenheight-pygame.Surface.get_height(ballimg)) 
    ball = GameObject(ballimg, spx, spy, starty)
    balls.append(ball)

# Create a ball object that the user will control
myballimg = pygame.image.load('myball.png').convert_alpha()
myball = GameObject(myballimg, 0, 0, screenwidth/2-pygame.Surface.get_width(myballimg)/2)

#frame = 0
while True:
    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN:
            match event.key:
                case pygame.K_UP:
                    myball.speedy = adjust_speed(myball.speedy, -1)
                    print(f"Speed y to {abs(myball.speedy)}\n")
                case pygame.K_DOWN:
                    myball.speedy = adjust_speed(myball.speedy, 1)
                    print(f"Speed y to {abs(myball.speedy)}\n")
                case pygame.K_LEFT:
                    myball.speedx = adjust_speed(myball.speedx, -1)
                    print(f"Speed x to {abs(myball.speedx)}\n")
                case pygame.K_RIGHT:
                    myball.speedx = adjust_speed(myball.speedx, 1)
                    print(f"Speed x to {abs(myball.speedx)}\n")

        if event.type==pygame.QUIT:
            sys.exit()

    # Redraw the background
    # screen.blit(background, position, position)
    screen.blit(background, (0, 0))
    # screen.fill(black)

    for ball in balls:
        moveball(ball, ballimg)
    moveball(myball, myballimg)

    pygame.display.update()
    # pygame.display.flip()
    #if frame==20:
    #    print(f"Position {ball.pos.x}, {ball.pos.y}")
    #    frame = 0
    #frame += 1

    clock.tick(60)
