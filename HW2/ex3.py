import turtle
import math as np
from random import *

turtle.speed(10)
turtle.shape('circle')
x=-500
y=0
dt=0.01
vx=200.0
vy=50.0
k=0.2
g=10
for i in range (0, 2000, 1):
	if y<0 and vy<0:
		vy=-vy*0.8
	x+=vx*dt
	y+=vy*dt-g*dt*dt/2.0
	vx+=-vx*k*dt
	vy+=(-vy*k-g)*dt
	turtle.goto(x, y)

