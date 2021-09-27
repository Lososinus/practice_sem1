import turtle

turtle.shape('turtle')
for i in range(10, 210, 20):
	turtle.forward(i)
	turtle.left(90)
	turtle.forward(i)
	turtle.left(90)
	turtle.forward(i+10)
	turtle.left(90)
	turtle.forward(i+10)
	turtle.left(90)
