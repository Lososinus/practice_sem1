import turtle
import numpy as np

def circ(r):
	for i in range(0, 90, 1):
		turtle.left(2)
		turtle.forward(r)
		turtle.left(2)

turtle.shape('turtle')
r = 1
turtle.left(90)
for i in range(5, 10, 1):
	circ(r*i)
	circ(-r*i)
