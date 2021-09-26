import turtle
import numpy as np

def poly(n, r):
	turtle.left(90+180.0/n)
	for i in range(0, n, 1):
		turtle.forward(2*r*np.sin(np.pi/n))
		turtle.left(360.0/n)
	turtle.right(90+180.0/n)
	
		

turtle.shape('turtle')
for i in range(3, 14, 1):
	r=i*15
	turtle.penup()
	turtle.forward(15)
	turtle.pendown()
	poly(i, r)
