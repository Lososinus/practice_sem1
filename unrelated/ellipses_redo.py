from random import random as random
from random import randint as randint
import pygame as pg
import numpy as np
import pygame.freetype as ft

def draw_lineABC(screen, width, hight, color, A, B, C):
	#рисует линию Ax+Bx+C=0
	tmp = 0
	if -C*B>0 and -C*B<hight*B*B:
		x1 = 0
		y1 = -C/B
		tmp+=1
	if -C*A>0 and -C*A<width*A*A:
		if tmp == 0:
			x1 = -C/A
			y1 = 0
		else:
			x2 = -C/A
			y2 = 0
		tmp+=1
	if -(C+A*width)*B>0 and -(C+A*width)*B<hight*B*B:
		if tmp == 0:
			x1 = width
			y1 = -(C+A*width)/B
		else:
			x2 = width
			y2 = -(C+A*width)/B
		tmp+=1
	if -(C+B*hight)*A>0 and -(C+B*hight)*A<width*A*A:
		if tmp == 0:
			x1 = -(C+B*hight)/A
			y1 = hight
		else:
			x2 = -(C+B*hight)/A
			y2 = hight
		tmp+=1
	if tmp >= 2:
		pg.draw.line(screen, color, (x1, y1), (x2, y2))

def draw_ell(screen, a, b, color, x, y, alph):
	tmp_srf = pg.Surface((round(2*a), round(2*b)))
	tmp_srf.set_colorkey((0, 0, 0))
	pg.draw.ellipse(tmp_srf, color, (0, 0, 2*a, 2*b))
	pg.draw.ellipse(tmp_srf, (200, 200, 200), (0, 0, 2*a, 2*b), 3)
	tmp_srf = pg.transform.rotate(tmp_srf, alph*180/np.pi)
	screen.blit(tmp_srf, (x-tmp_srf.get_width()/2, y-tmp_srf.get_height()/2))
#константы
n = 1
max_fps = 30
width = 1080
hight = 1800
g = -200
f_forward = 1.0
a0 = 200.0
b0 = 100.0
#массивы лол
a = [a0] * n
b = [b0] * n
m = [1.0] * n
j = [(a[i]**2+b[i]**2)*m[i]*0.25 for i in range(n)]
x = [width*0.5] * n
y = [hight*0.2] * n
alph = [1.0] * n
vx = [0.0] * n
vy = [0.0] * n
omeg = [0.0] * n
color = [(175, 0, 0)] * n
#стены в виде Ax+By+C=0
wall_amm = 6
A = [0, 1, 0, 1, 4, 4]
B = [1, 0, 1, 0, 4, -4]
C = [-1, 1-width, 1-hight, -1, -3*width-4*hight, -width+4*hight]
#инициализация pygame
pg.init()
screen = pg.display.set_mode((width, hight))
clock = pg.time.Clock()
ft.init()
font = ft.Font(file="Anonymous_Pro.ttf", size=60, font_index=0, resolution=0, ucs4=False)
finished = False
#осн цикл
dt=0
delta_t=0
while not finished:
	for i in range(n):
		sin_alph = np.sin(alph[i])
		cos_alph = np.cos(alph[i])
#		for k in range(wall_amm):
#			coll_ellipse_line(a[i], b[i], j[i]/m[i], x[i], y[i], alph[i], vx[i], vy[i], omeg[i], A[k], B[k], C[k])
		
#		calc_iter(x[i], y[i], alph[i], vx[i], vy[i], omeg[i], dt*f_forward, g)
		
	
	
	for i in range(n):
		draw_ell(screen, a[i], b[i], color[i], x[i], y[i], alph[i])
	for k in range(wall_amm):
		draw_lineABC(screen, width, hight, (220, 220, 220), A[k], B[k], C[k])
	draw_lineABC(screen, width, hight, (220, 220, 220), 1, -1, 0)
	pg.display.update()
	screen.fill((0, 0, 0), (0, 0, width, hight+300))
	
	for event in pg.event.get():
		if event.type == pg.QUIT:
			finished = True
	
	delta_t = clock.tick(max_fps)
	dt = delta_t/1000

pg.quit()
ft.quit()