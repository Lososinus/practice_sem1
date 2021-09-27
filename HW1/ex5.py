import turtle

turtle.shape('turtle')
for i in range(10, 110, 10):
	turtle.forward(i)
	turtle.left(90)
	turtle.forward(i)
	turtle.left(90)
	turtle.forward(i)
	turtle.left(90)
	turtle.forward(i)
	turtle.penup()
	turtle.forward(5)
	turtle.left(90)
	turtle.forward(-5)
	turtle.pendown()
