import turtle
import numpy as np

def poly(n, r):
	turtle.left(90+180.0/n)
	for i in range(0, n, 1):
		turtle.forward(2*r*np.sin(np.pi/n))
		turtle.left(360.0/n)
	turtle.right(90+180.0/n)

def circ(r):
	poly(30, r)
	
def arc(r):
	n=30
	turtle.left(90+180.0/n)
	for i in range(0, n//2, 1):
		turtle.forward(2*r*np.sin(np.pi/n))
		turtle.left(360.0/n)
	turtle.right(90+180.0/n)

turtle.shape('turtle')
turtle.left(90)

turtle.penup()
turtle.forward(100)
turtle.pendown()
circ(100)
turtle.penup()

turtle.goto(40,60)
turtle.pendown()
circ(20)
turtle.penup()
turtle.goto(-40,60)
turtle.pendown()
circ(20)
turtle.penup()

turtle.goto(0,0)
turtle.pendown()
turtle.forward(30)
turtle.penup()

turtle.goto(-40,-20)
turtle.pendown()
turtle.left(90)
arc(40)
turtle.penup()
