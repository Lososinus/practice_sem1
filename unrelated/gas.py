from random import *
import pygame
import pygame.freetype
import numpy as np
from pygame.draw import *

def soft_check(n, x, y, r, wx, wy):
        #возвращает множество пар - номера частиц чьи проекции на (wx, wy) пересекаются.
        segment = [(0,0,0)] * n
        for i in range(n):
                proj = x[i]*wx+y[i]*wy
                segment[i] = (proj-r[i], proj+r[i], i)
        segment.sort()
    
        intersect = set()
        for i in range(n-1):
                k=i+1
                while (k<n and segment[i][1]>segment[k][0]):
                        intersect.add((min(segment[i][2], segment[k][2]), max(segment[i][2], segment[k][2])))
                        k+=1
        return intersect

def strict_check(intersect, n, r, x, y):
	#оставляет только действительно пересекающиеся окружности
	collisions = set()
	for pair in intersect:
		i = pair[0]
		k = pair[1]
		if ((x[i]-x[k])**2 + (y[i]-y[k])**2 < (r[i]+r[k])**2):
			collisions.add((min(i, k), max(i, k)))
	return collisions

def calc_coll_gas(collision, n, m, x, y, vx, vy,):
	#вычисляет скорости частиц после столкновений между собой
	for pair in collision:
		x1 = x[pair[0]]
		y1 = y[pair[0]]
		vx1 = vx[pair[0]]
		vy1 = vy[pair[0]]
		x2 = x[pair[1]]
		y2 = y[pair[1]]
		vx2 = vx[pair[1]]
		vy2 = vy[pair[1]]
		factor1 = (vx2-vx1)*(x2-x1) + (vy2-vy1)*(y2-y1)
		if (factor1 < 0):
			factor2  = 2.0*factor1/((m[pair[0]]+m[pair[1]]) * ((x2-x1)**2 + (y2-y1)**2))
			vx[pair[0]]+=m[pair[1]]*factor2*(x2-x1)
			vy[pair[0]]+=m[pair[1]]*factor2*(y2-y1)
			vx[pair[1]]+=m[pair[0]]*factor2*(x1-x2)
			vy[pair[1]]+=m[pair[0]]*factor2*(y1-y2)

def calc_coll_walls(width, hight, n, r, x, y, vx, vy):
	#обрабатывает столкновения со стенами
	for i in range(n):
		if vx[i]>0 and x[i]+r[i]>width:
			vx[i]*= -1.0
		if vy[i]>0 and y[i]+r[i]>hight:
			vy[i]*= -1.0
		if vx[i]<0 and x[i]-r[i]<0:
			vx[i]*= -1.0
		if vy[i]<0 and y[i]-r[i]<0:
			vy[i]*= -1.0

def calc_itr(n, x, y, vx, vy, dt, g):
	#обрабатывает итерацию движения частиц за dt
	for i in range(n):
		x[i]+=vx[i]*dt
		y[i]+=vy[i]*dt-g*dt**2/2
		vy[i]-=g*dt

def drawgas(screen, n, x, y, r, color, width, hight):
	# отрисовка частиц
	for i in range(n):
		circle(screen, color[i], (round(x[i]), round(y[i])), round(r[i]))

def drawgas_blurred(screen, n, x, y, r, color, width, hight):
	# отрисовка следа частиц
	for i in range(n):
		r_int = round(r[i])
		tmp_surf = pygame.Surface((2*r_int, 2*r_int))
		circle(tmp_surf, color[i], (r_int, r_int), r_int)
		tmp_surf.set_colorkey((0, 0, 0))
		tmp_surf.set_alpha(3)
		screen.blit(tmp_surf, (round(x[i]-r[i]), round(y[i]-r[i])))

def draw_chart(screen, x1, y1, x2, y2, stat, n):
	#простенький график без обозначений
	screen.fill((0, 0, 0), (x1, y1, x2-x1, y2-y1))
	bold = 3
	work_x = x2-x1-2*bold
	work_y = y2-y1-2*bold
	ed_x = x1 + bold
	ed_y = y2 - bold
	rect(screen, (100, 230, 100), (x1+bold, y1+bold, work_x, work_y), 2)
	mx = 1
	for i in range(n):
		mx = max(mx, stat[i])
	dot = [(0, 0)] * n
	for i in range(n):
		dot[i] = (ed_x + work_x*i/(n-1), ed_y - work_y*stat[i]/(mx))
	lines(screen, (100, 100, 230), 0, dot, 1)

#константы
max_fps = 0
n = 400
width = 1000
hight = 800
g = -200
r0 = 10
f_forward = 1.0
#инициализация частиц газа
r = [r0] * n
m =  [1.0] * n
x = [width*0.5] * n
y = [hight*0.5] * n
vx = [0.0] * n
vy = [0.0] * n
color = [(120, 255, 240)] * n
for i in range(n):
    x[i]+=(random()-0.5)*width
    y[i]+=(random()-0.5)*hight
    vx[i] = (2*random()-1)*400
    vy[i] = (2*random()-1)*400
#инициализация визуализации
pygame.init()
pygame.freetype.init()
screen = pygame.display.set_mode((width, hight+200))
clock = pygame.time.Clock()
subclock = pygame.time.Clock()
finished = False
font = pygame.freetype.Font(file="Anonymous_Pro.ttf", size=50, font_index=0, resolution=0, ucs4=False)
#осн цикл
st_size = 50
vx_stat=[0.0]*(st_size*2+1)
delta_t = 0
dt_draw = 0
dt_compute = 0
dt_write = 0
fps = 0
itr=0
gas = pygame.Surface((width, hight))
gas.set_alpha(250)
dt = 0
while not finished:
	subclock.tick()
	rand_tg = np.tan((random()-0.5)*np.pi)
	wx = (1+rand_tg**2)**-0.5
	wy = rand_tg*wx
	intersect = soft_check(n, x, y, r, wx, wy)
	collision = strict_check(intersect, n, r, x, y)
	calc_coll_gas(collision, n, m, x, y, vx, vy,)
	calc_coll_walls(width, hight, n, r, x, y, vx, vy)
	calc_itr(n, x, y, vx, vy, dt*f_forward, g)
	for i in range(n):
		v_2 = (vx[i]**2+vy[i]**2)/200000
		c = v_2**2/(1+v_2**2)*255
		color[i] = (c, 0, 255-c)
	for i in range(st_size*2+1):
		vx_stat[i]*=0.995
	for i in range(n):
		vx_stat[min(max(round(vx[i]/30)+st_size, 0), st_size*2)]+=1
	dt_compute = subclock.tick()
	
	screen.fill((0, 0, 0), (0, 0, width, hight))
	drawgas_blurred(gas, n, x, y, r, color, width, hight)
	screen.blit(gas, (0,0))
	drawgas(screen, n, x, y, r, color, width, hight)
	dt_draw = subclock.tick()
	
	font.render_to(screen, (10, hight+50*0), "fps:      {0:8.2f} itr: {1:5d}".format(fps, itr), (232, 98, 129), (0, 0, 0))
	font.render_to(screen, (10, hight+50*1), "physics time: {0:4d}".format(dt_compute), (232, 98, 129), (0, 0, 0))
	font.render_to(screen, (10, hight+50*2), "drawgas time: {0:4d}".format(dt_draw), (232, 98, 129), (0, 0, 0))
	font.render_to(screen, (10, hight+50*3), "write time:   {0:4d}".format(dt_write), (232, 98, 129), (0, 0, 0))
	font.render_to(screen, (10, hight+50*4), "total time:   {0:4d}".format(delta_t), (232, 98, 129), (0, 0, 0))
	draw_chart(screen, 600, hight+50*1, width, hight+200, vx_stat, st_size*2+1)
	dt_write = subclock.tick()
	
	#line(screen, (200, 200, 200), (width/2-wx*400, hight/2-wy*400), (width/2+wx*400, hight/2+wy*400))
	pygame.display.update()
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			finished = True
	delta_t = clock.tick(max_fps)
	dt = delta_t/1000
	fps = clock.get_fps()
	itr+=1
	
pygame.freetype.quit()
pygame.quit()
