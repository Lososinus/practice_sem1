import turtle
import math as np
from random import *

def drawdigit(digit, size):
	angl=0
	x=0
	y=0
	digit=digit+[[2, 0, 0]]
	for dot in digit:
		print(dot)
		if (x!=dot[0]) or (y!=dot[1]):
			if dot[2]:
				turtle.pendown()
			else:
				turtle.penup()
			lth=size*((x-dot[0])**2+(y-dot[1])**2)**0.5
			azimuth=np.atan2(dot[0]-x, y-dot[1])
			x=dot[0]
			y=dot[1]
			print(azimuth, "  ", angl)
			turtle.right((azimuth-angl)*180.0/np.pi)
			angl=azimuth
			turtle.forward(lth)
	turtle.left(angl*180.0/np.pi)
			
			
	
def drawindex(digits, index, size):
	for digit in index:
		if '0'<=digit<='9':
			drawdigit(digits[ord(digit)-ord('0')], size)

turtle.penup()
turtle.goto(-300, 0)
turtle.left(100)
dig0=[[0, 2, 1], [1, 2, 1], [1, 0, 1], [0, 0, 1]]
dig1=[[0, 1, 0], [1, 0, 1], [1, 2, 1]]
dig2=[[1, 0, 1], [1, 1, 1], [0, 2, 1], [1, 2, 1]]
dig3=[[1, 0, 1], [0, 1, 1], [1, 1, 1], [0, 2, 1]]
dig4=[[0, 1, 1], [1, 1, 1], [1, 2, 1], [1, 0, 1]]
dig5=[[0, 2, 0], [1, 2, 1], [1, 1, 1], [0, 1, 1], [0, 0, 1], [1, 0, 1]]
dig6=[[0, 1, 0], [0, 2, 1], [1, 2, 1], [1, 1, 1], [0, 1, 1], [1, 0, 1]]
dig7=[[1, 0, 1], [0, 1, 1], [0, 2, 1]]
dig8=[[0, 2, 1], [1, 2, 1], [1, 0, 1], [0, 0, 1], [0, 1, 0], [1, 1, 1]]
dig9=[[1, 1, 0], [1, 0, 1], [0, 0, 1], [0, 1, 1], [1, 1, 1], [0, 2, 1]]
digits=[dig0, dig1, dig2, dig3, dig4, dig5, dig6, dig7, dig8, dig9]
turtle.shape('turtle')

index="1234567890"
size=40
drawindex(digits, index, size)
