import turtle
import numpy as np

def circ(r):
	for i in range(0, 90, 1):
		turtle.left(2)
		turtle.forward(r)
		turtle.left(2)


turtle.shape('turtle')
r = 5
for i in range(0, 5, 1):
	circ(r)
	circ(-r)
	turtle.left(72)
