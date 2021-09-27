import turtle
import numpy as np

turtle.shape('turtle')
a = 10
for t in range(0, 360*10, 1):
	turtle.goto(a*t/360.0*np.cos(t/180*np.pi), a*t/360.0*np.sin(t/180*np.pi))
	turtle.right(1)
