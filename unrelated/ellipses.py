from random import *
import pygame
import pygame.freetype
from pygame.draw import *
import numpy as np

def coll_basic(j, vx, vy, omeg, rx, ry, ax, ay):
	#вычисляет скорость после удара о твёрдую стенку. Прямая удара задана как r+at, с началом координат в цм тела.
	comm_fac = 2.0*((vx-omeg*ry)*ax+(vy+omeg*rx)*ay)/(j*(ax**2+ay**2)+(rx*ay-ry*ax)**2)
	vx_ans = vx - j*ax*comm_fac
	vy_ans = vy - j*ay*comm_fac
	omeg_ans = omeg - (rx*ay-ry*ax)*comm_fac
	return vx, vy, omeg



def calc_coll_walls(width, hight, n, a, b, x, y, alph, vx, vy, omeg):
	#обрабатывает столкновения со стенами
	for i in range(n):
		cos_sqr = np.cos(alph[i])**2
		sin_sqr = 1-cos_sqr
		el_width = (a[i]**2*cos_sqr+b[i]**2*sin_sqr)**0.5
		el_hight = (a[i]**2*sin_sqr+b[i]**2*cos_sqr)**0.5
		factor = (a[i]**2-b[i]**2)*0.5*np.sin(2*alph[i])
		el_width_dot = -factor*omeg[i]/el_width
		el_hight_dot = +factor*omeg[i]/el_hight
		j=(a[i]**2+b[i]**2)*0.25
		
		if vx[i]+el_width_dot>0 and x[i]+el_width>width:
			impameter = -factor/el_width
			factor_2 = 2*(vx[i]+omeg[i]*impameter)/(j+impameter**2)
			line(screen, (200, 200, 200), (0, impameter+y[i]), (width, impameter+y[i]))
			vx[i]-=j*factor_2
			omeg[i]-=impameter*factor_2
		
		if vy[i]+el_hight_dot>0 and y[i]+el_hight>hight:
			impameter = -factor/el_hight
			factor_2 = 2*(vy[i]-omeg[i]*impameter)/(j+impameter**2)
			line(screen, (200, 200, 200), (impameter+x[i], 0), (impameter+x[i], hight))
			vy[i]-=j*factor_2
			omeg[i]+=impameter*factor_2
		
		if vx[i]-el_width_dot<0 and x[i]-el_width<0:
			impameter = factor/el_width
			factor_2 = 2*(vx[i]+omeg[i]*impameter)/(j+impameter**2)
			line(screen, (200, 200, 200), (0, impameter+y[i]), (width, impameter+y[i]))
			vx[i]-=j*factor_2
			omeg[i]-=impameter*factor_2
		
		if vy[i]-el_hight_dot<0 and y[i]-el_hight<0:
			impameter = factor/el_hight
			factor_2 = 2*(vy[i]-omeg[i]*impameter)/(j+impameter**2)
			line(screen, (200, 200, 200), (impameter+x[i], 0), (impameter+x[i], hight))
			vy[i]-=j*factor_2
			omeg[i]+=impameter*factor_2

def calc_iter(n, x, y, alph, vx, vy, omeg, dt, g):
	#обрабатывает итерацию движения частиц за dt
	for i in range(n):
		x[i]+=vx[i]*dt
		y[i]+=vy[i]*dt-g*dt**2/2
		alph[i]+=omeg[i]*dt
		vy[i]-=g*dt

def drawgas(screen, n, a, b, x, y, alph, color, width, hight):
	# отрисовка эллипсов
	rect(screen, (200, 200, 200), (0, 0, width, hight), 2)
	for i in range(n):
		tmp_surf = pygame.Surface((round(2*a[i]), round(2*b[i])))
		tmp_surf.set_colorkey((0, 0, 0))
		ellipse(tmp_surf, color[i], (0, 0, 2*a[i], 2*b[i]))
		ellipse(tmp_surf, (200, 200, 200), (0, 0, 2*a[i], 2*b[i]), 3)
		tmp_surf = pygame.transform.rotate(tmp_surf, alph[i]*180/np.pi)
		screen.blit(tmp_surf, (x[i]-tmp_surf.get_width()/2, y[i]-tmp_surf.get_height()/2))

#константы
max_fps = 30
n = 3
width = 1080
height = 1800
g = -200
a0 = 200
b0 = 50
f_forward = 1.0
#инициализация частиц газа
a = [a0] * n
b = [b0] * n
m =  [1.0] * n
x = [width*0.5] * n
y = [height*0.2] * n
alph = [0.0] * n
vx = [0.0] * n
vy = [0.0] * n
omeg = [0.0] * n
color = [(175, 0, 0)] * n
for i in range(n):
    a[i] = -100*i+300
    x[i] += (random()-0.5)*width*0
    y[i] += (random()-0.5)*height*0
    alph[i] = 2*np.pi*random()
    vx[i] = (2*random()-1)*200
    vy[i] = (2*random()-1)*200
    omeg[i] =(2*random()-1)*5
#инициализация визуализации
pygame.init()
pygame.freetype.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
subclock = pygame.time.Clock()
finished = False
font = pygame.freetype.Font(file="Anonymous_Pro.ttf", size=60, font_index=0, resolution=0, ucs4=False)
#осн цикл
delta_t = 0
dt_draw = 0
dt_compute = 0
dt_write = 0
fps = 0
iter=0
dt = 0
while not finished:
	subclock.tick()
	calc_coll_walls(width, height, n, a, b, x, y, alph, vx, vy, omeg)
	calc_iter(n, x, y, alph, vx, vy, omeg, dt*f_forward, g)
	dt_compute = subclock.tick()
	
	drawgas(screen, n, a, b, x, y, alph, color, width, height)
	dt_draw = subclock.tick()
	
	font.render_to(screen, (10, 1810), "fps:      {0:8.2f} iter: {1:5d}".format(fps, iter), (232, 98, 129), (0, 0, 0))
	font.render_to(screen, (10, 1870), "x:  {0:6.1f}   vx: {1:3.3f}".format(x[0], vx[0]), (232, 98, 129), (0, 0, 0))
	font.render_to(screen, (10, 1930), "y:  {0:6.1f}   vy: {1:3.3f}".format(y[0], vy[0]), (232, 98, 129), (0, 0, 0))
	font.render_to(screen, (10, 1990), "alph: {0:1.2f}    omeg: {1:2.2f}".format(alph[0]-2*np.pi*round(alph[0]/(2*np.pi)-0.5), omeg[0]), (232, 98, 129), (0, 0, 0))
	font.render_to(screen, (10, 2050), "ener:    {0:15.6f}".format(vx[0]**2+vy[0]**2+(a[0]**2+b[0]**2)*omeg[0]**2/4+2*g*(y[0]-height)), (232, 98, 129), (0, 0, 0))
	dt_write = subclock.tick()
	
	pygame.display.update()
	screen.fill((0, 0, 0), (0, 0, 1080, 2140))
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			finished = True
	
	delta_t = clock.tick(max_fps)
	dt = delta_t/1000
	fps = clock.get_fps()
	iter+=1

pygame.freetype.quit()
pygame.quit()