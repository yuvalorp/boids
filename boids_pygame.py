import pygame
import time
from random import choice,seed
from random import randint as random
from copy import copy
from birds import *

pygame.init()
#colors 
display_width = 800
display_height = 800
white = (255,255,255)


 
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('boids')
clock = pygame.time.Clock()

pause = False

 

def quitgame():
    pygame.quit()
    quit()

def game_loop():
    gameExit = False
    frame=0
    df=0
    max_frame=len(bL[0].pL)
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    df= 1
                if event.key == pygame.K_RIGHT:
                    df=-1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:

                    df= 0
        frame+=df
        
        if (max_frame-1)<=frame:
            frame=0
        if 0>frame:
            frame=max_frame-2
            
        gameDisplay.fill(white)
        for b in bL:
            place=b.pL[frame]
            place=[place[0]*5+100,place[1]*5+100]

            if b.name=="eagle":
                pygame.draw.circle(gameDisplay, (0, 255, 0), place, 3)

                for v in b.f_list[frame]:
                    v2=[v[0]*5+100,v[1]*5+100]
                    pygame.draw.line(gameDisplay, (0, 255, 255),  place, v2, width=1)
            elif b.name=="1":
                pygame.draw.circle(gameDisplay, (255, 0, 0), place, 3)

            else:
                pygame.draw.circle(gameDisplay, (0,0,255),place, 2)

        pygame.display.update()
        clock.tick(15)


the_seed=random(0,1000)
seed(the_seed)
#seed(9)
print(the_seed)
#cohesion,alignment,Separation,follow,escape

bL= [bird([random(0,20),random(0,20)],1.5,[0.3,0.3,0.9,0.1,1]) for i in range(20)]

bL+=[eagle([10,-30],2,[0.9,0.1,0.1],n="eagle")]


t=0
dt=0.5
while t<100:
    for b in bL:
        b.np(bL,dt,t)
    t+=dt

#print(bL[-1].f_list)
game_loop()
quitgame()
