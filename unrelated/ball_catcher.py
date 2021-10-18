from random import random
from random import randint
import pygame as pg
import numpy as np
import pygame.freetype as ft

#константы
max_fps = 30
width = 1500
hight = 900
#инициализация pygame
pg.init()
screen = pg.display.set_mode((width, hight))
clock = pg.time.Clock()
ft.init()
font = ft.Font(file="Anonymous_Pro.ttf", size=50)
finished = False
#осн цикл
dt = 0
delta_t = 0
while not finished:
	pg.draw.rect(screen, (200, 200, 200), (100, 100, 1000, 700), 1)
	pg.draw.rect(screen, (200, 200, 200), (200, 25, 100, 50), 1)
	pg.draw.rect(screen, (200, 200, 200), (1000, 25, 100, 50), 1)
	pg.draw.rect(screen, (200, 200, 200), (1300, 25, 150, 50), 1)
	pg.draw.rect(screen, (200, 200, 200), (1150, 150, 100, 100), 1)
	pg.draw.rect(screen, (200, 200, 200), (1250, 150, 100, 100), 1)
	pg.draw.rect(screen, (200, 200, 200), (1350, 150, 100, 100), 1)
	pg.draw.rect(screen, (200, 200, 200), (1150, 350, 50, 200), 1)
	pg.draw.rect(screen, (200, 200, 200), (1150, 650, 50, 150), 1)
	pg.draw.rect(screen, (200, 200, 200), (1250, 650, 50, 150), 1)

	pg.display.update()
	screen.fill((0, 0, 0))
	
	for event in pg.event.get():
		if event.type == pg.QUIT:
			finished = True
	
	delta_t = clock.tick(max_fps)
	dt = delta_t/1000

pg.quit()
ft.quit()
