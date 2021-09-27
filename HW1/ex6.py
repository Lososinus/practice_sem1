import turtle

turtle.shape('turtle')
n = 50
for i in range(0, n, 1):
	turtle.forward(100)
	turtle.stamp()
	turtle.forward(-100)
	turtle.left(360.0/n)
