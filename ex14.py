import turtle
import numpy as np

def poly(n, r):
	for i in range(0, n, 1):
		turtle.forward(2*r*np.sin(np.pi/2*(1-1.0/n)))
		turtle.right(180.0*(1-1.0/n))

turtle.shape('turtle')
r=50
poly(5, r)
turtle.penup()
turtle.forward(150)
turtle.pendown()
poly(11, r)
