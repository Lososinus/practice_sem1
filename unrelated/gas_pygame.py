from random import *
import pygame
from pygame.draw import *

def soft_check(n, x, r):
        #создаёт множество пар - номера отрезков пересекающихся отрезков с центром х и длиной 2r
        segment = []
        for i in range(n):
                seg = (x[i]-r[i], x[i]+r[i], i)
                segment.append(seg)
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
			factor2  = 2*factor1/((m[pair[0]]+m[pair[1]]) * ((x2-x1)**2 + (y2-y1)**2))
			vx[pair[0]]+=m[pair[1]]*factor2*(x2-x1)
			vy[pair[0]]+=m[pair[1]]*factor2*(y2-y1)
			vx[pair[1]]+=m[pair[0]]*factor2*(x1-x2)
			vy[pair[1]]+=m[pair[0]]*factor2*(y1-y2)

def calc_coll_walls(width, height, n, r, x, y, vx, vy):
	#обрабатывает столкновения со стенами
	for i in range(n):
		if (vx[i]>0 and x[i]+r[i]>width):
			vx[i]*=-1.0
		if vy[i]>0 and y[i]+r[i]>height:
			vy[i]*=-1.0
		if vx[i]<0 and x[i]-r[i]<0:
			vx[i]*=-1.0
		if vy[i]<0 and y[i]-r[i]<0:
			vy[i]*=-1.0

def calc_iter(n, x, y, vx, vy, dt, g):
	#обрабатывает итерацию движения частиц за dt
	for i in range(n):
		x[i]+=vx[i]*dt
		y[i]+=vy[i]*dt-g*dt**2/2
		vy[i]-=g*dt

def drawgas(screen, n, x, y, width, height):
	# отрисовка частиц
	rect(screen, (255, 255, 255), (0, 0, width, height))
	rect(screen, (0, 0, 0), (0, 0, width, height), 3)
	for i in range(n):
		circle(screen, (50, 80, 50), (x[i], y[i]), r[i], 5)

#константы
FPS = 40
n = 100
width = 1000
height = 1000
dt = 0.025
g = 0.1

#инициализация частиц газа
r = [20.0] * n
print(n)
m =  [1.0] * n
x = [width/2] * n
y = [height/2] * n
vx = [0.0] * n
vy = [0.0] * n
for i in range(n):
    vx[i] = (2.0*random()-1.0)*500.0
    vy[i] = (2.0*random()-1.0)*0.00000001

pygame.init()
screen = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()
finished = False

while not finished:
	intersect_x = soft_check(n, x, r)
	intersect_y = soft_check(n, y, r)
	intersect = intersect_x & intersect_y
	collision = strict_check(intersect, n, r, x, y)
	calc_coll_gas(collision, n, m, x, y, vx, vy,)
	calc_coll_walls(width, height, n, r, x, y, vx, vy)
	calc_iter(n, x, y, vx, vy, dt, g)
	drawgas(screen, n, x, y, width, height)
	pygame.display.update()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			finished = True
	clock.tick(FPS)

pygame.quit()