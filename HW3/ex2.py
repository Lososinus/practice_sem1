import pygame
from pygame.draw import *

def stick_sticker(screen, sticker, x1, y1, x2, y2):
	if x1>x2:
		x1, x2 = x2, x1
		sticker = pygame.transform.flip(sticker, True, False)
	if y1>y2:
		y1, y2 = y2, y1
		sticker = pygame.transform.flip(sticker, False, True)
	sticker = pygame.transform.scale(sticker, (x2-x1, y2-y1))
	screen.blit(sticker, (x1, y1)) 

def fence():
	image = pygame.Surface((1000, 400))
	rect(image, (220, 220, 80), (0, 0, 1000, 400))
	N=15
	for i in range(1, N):
		line(image, (0, 0, 0), (1000*i/N, 0), (1000*i/N, 400), 3)
	return image

def shack():
	image = pygame.Surface((400, 400))
	image.set_colorkey((0, 0, 0))	

	polygon(image, (180, 180, 60), ((300, 400), (150, 350), (150, 150), (300, 175)))
	polygon(image, (60, 50, 20), ((300, 400), (150, 350), (150, 150), (300, 175)), 3)
	polygon(image, (180, 180, 60), ((300, 400), (350, 320), (350, 150), (300, 175)))
	polygon(image, (60, 50, 20), ((300, 400), (350, 320), (350, 150), (300, 175)), 3)
	polygon(image, (180, 180, 60), ((225, 50), (150, 150), (300, 175)))
	polygon(image, (60, 50, 20), ((225, 50), (150, 150), (300, 175)), 3)
	polygon(image, (180, 180, 60), ((225, 50), (275, 25), (350, 150), (300, 175)))
	polygon(image, (60, 50, 20), ((225, 50), (275, 25), (350, 150), (300, 175)), 3)
	ellipse(image, (1, 1, 1), (180, 220, 100, 90))
	
	ellipse(image, (1, 1, 1), (180, 290, 30, 20), 2)
	return image
		
def background():
	image = pygame.Surface((1000, 1000))

	polygon(image, (50, 50, 230), ((0, 0), (1000, 0), (1000, 600), (0, 600)))
	polygon(image, (50, 200, 50), ((0, 600), (1000, 600), (1000, 1000), (0, 1000)))
	stick_sticker(image, fence(), 0, 200, 1000, 600)
	stick_sticker(image, shack(), 500, 500, 900, 900)

	return image
		
def dog():
	image = pygame.Surface((1000, 1000))
	
		
	
	return image

pygame.init()

FPS = 30
screen = pygame.display.set_mode((1000, 1000))

stick_sticker(screen, background(), 0, 0, 1000, 1000)


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
