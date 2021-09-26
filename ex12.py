import turtle
import numpy as np

def arc(r):
	for i in range(0, 30, 1):
		turtle.right(3)
		turtle.forward(r)
		turtle.right(3)

turtle.shape('turtle')
r = 1
turtle.left(90)
for i in range(0, 5, 1):
	arc(r*5)
	arc(r)
