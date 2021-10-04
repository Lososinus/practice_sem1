import pygame
from pygame.draw import *

def fence(screen, x1, y1, x2, y2):
	rect(screen, (220, 220, 60), (x1, y1, x2-x1, y2-y1))
	N=15
	for i in range(1, N):
		line(screen, (0, 0, 0), (x1+(x2-x1)*i/N, y1), (x1+(x2-x1)*i/N, y2), 2)
		
def background(screen, x1, y1, x2, y2):
	polygon(screen, (50, 50, 255), [(x1, y1), (x1, y1+(y2-y1)*0.2), (x2, y1+(y2-y1)*0.2), (x2, y1)])
	polygon(screen, (50, 255, 50), [(x1, y1+(y2-y1)*0.6), (x1, y1+(y2-y1)*1.0), (x2, y1+(y2-y1)*1.0), (x2, y1+(y2-y1)*0.6)])
	fence(screen, x1, y1+(y2-y1)*0.2, x2, y1+(y2-y1)*0.6)
		
def dog(screen, x1, y1, x2, y2):
	pass

pygame.init()

FPS = 30
screen = pygame.display.set_mode((1000, 1000))

background(screen, 0, 0, 1000, 1000)
dog(screen, 100, 700, 300, 200)

#arc(screen, (255, 255, 255), (100, 100, 50, 50), 0, 1, 1)


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()