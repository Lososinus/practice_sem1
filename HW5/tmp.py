from random import random
from random import randint
import pygame as pg
import numpy as np

class Button:
    pg.init()
    whitebox_0 = pg.Surface((200, 200))
    pg.draw.line(whitebox_0, (200, 200, 200), (0, 0), (199, 0))
    pg.draw.line(whitebox_0, (200, 200, 200), (199, 0), (199, 199))
    pg.draw.line(whitebox_0, (200, 200, 200), (199, 199), (0, 199))
    pg.draw.line(whitebox_0, (200, 200, 200), (0, 199), (0, 0))
    whitebox_1 = whitebox_0.copy()
    pg.draw.line(whitebox_0, (200, 200, 200), (0, 0), (199, 199))
    pg.draw.line(whitebox_0, (200, 200, 200), (199, 0), (0, 199))
    
    def __init__ (self, x, y, w, h, sprite_0 = whitebox_0, sprite_1 = whitebox_1, state = False):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.sprite_0 = sprite_0
        self.sprite_1 = sprite_1
        self.state = state
    
    def click (self, x_click, y_click):
        if (self.x < x_click) & (self.x + self.w > x_click) & (self.y < y_click) & (self.y + self.h > y_click):
            self.state = not self.state
    
    def draw_butt (self, surface):
        if self.state:
            if (self.w, self.h) != self.sprite_1.get_size():
                self.sprite_1 = pg.transform.smoothscale(self.sprite_1, (self.w, self.h))
            surface.blit(self.sprite_1, (self.x, self.y))
        else:
            if (self.w, self.h) != self.sprite_0.get_size():
                self.sprite_0 = pg.transform.smoothscale(self.sprite_0, (self.w, self.h)) 
            surface.blit(self.sprite_0, (self.x, self.y))

def f():
	return 0, 21

# константы
max_fps = 20
width = 1600
hight = 600
# инициализация визуализации
pg.init()
screen = pg.display.set_mode((width, hight+200))
clock = pg.time.Clock()
finished = False
# кнопки
btn_1 = Button(0, hight, 150, 100)
# осн цикл
print(f()[1])
while not finished:
	btn_1.draw_butt(screen)
	pg.display.update()
	screen.fill((0, 0, 0), (0, 0, width, hight+200))
	
	for event in pg.event.get():
		if event.type == pg.QUIT:
			finished = True
		elif event.type == pg.MOUSEBUTTONDOWN:
		    btn_1.click(event.pos[0], event.pos[1])
	clock.tick(max_fps)

pg.quit()
