import turtle
import math as np
from random import *

def getfont(name):	
	digits = []
	size = 0
	input = open(name, 'r')
	s = input.readline()
	size = int(s.rstrip())
	for i in range (0, 10, 1):
		s = input.readline()
		s = s.rstrip()
		digits = digits + eval("[" + s + "]")
	input.close()
	return  (digits, size)
	

def drawdigit(digit, size):
	angl=0
	x=0
	y=0
	digit=digit+[[2, 0, 0]]
	for dot in digit:
		if (x!=dot[0]) or (y!=dot[1]):
			if dot[2]:
				turtle.pendown()
			else:
				turtle.penup()
			lth=size*((x-dot[0])**2+(y-dot[1])**2)**0.5
			azimuth=np.atan2(dot[0]-x, y-dot[1])
			x=dot[0]
			y=dot[1]
			turtle.right((azimuth-angl)*180.0/np.pi)
			angl=azimuth
			turtle.forward(lth)
	turtle.left(angl*180.0/np.pi)
			
			
	
def drawindex(digits, index, size):
	for digit in index:
		if '0'<=digit<='9':
			drawdigit(digits[ord(digit)-ord('0')], size)

digits, size = getfont("font")
turtle.penup()
turtle.goto(-300, 0)
turtle.left(90)
turtle.shape('turtle')

index = input()
drawindex(digits, index, size)
