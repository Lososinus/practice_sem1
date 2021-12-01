import matplotlib.pyplot as plt
import numpy as np

def runge_kutta (x_span, h):
    n = round(x_span/h)
    otv = ([0] * (n+1), [0] * (n+1), [0] * (n+1))
    
    x = 0
    y = 0.8
    z = 2

    otv[0][0] = x
    otv[1][0] = y
    otv[2][0] = z
    
    print("{0:e} {1:e} {2:e} ".format(x, y, z))
    k = 0
    for i in range(1, n+1, 1):	
        k1 = h * f(x, y, z)        
        q1 = h * g(x, y, z)

        k2 = h * f(x + h/2.0, y + q1/2.0, z + k1/2.0)
        q2 = h * g(x + h/2.0, y + q1/2.0, z + k1/2.0)

        k3 = h * f(x + h/2.0, y + q2/2.0, z + k2/2.0)
        q3 = h * g(x + h/2.0, y + q2/2.0, z + k2/2.0)

        k4 = h * f(x + h, y + q3, z + k3)
        q4 = h * g(x + h, y + q3, z + k3)

        z_next = z + (k1 + 2.0*k2 + 2.0*k3 + k4)/6.0
        y_next = y + (q1 + 2.0*q2 + 2.0*q3 + q4)/6.0
        
        if (i>(n*k)/10):
            k+=1
            print("{0:+10.6f}   {1:+10.6f}   {2:+10.6f} ".format(x, y, z))
        
        x = x + h
        y = y_next
        z = z_next
        
        otv[0][i] = x
        otv[1][i] = y
        otv[2][i] = z
        
    return otv

def f (x, y, z):
    return np.cos(3*x) - 4*y

def g (x, y, z):
    return z


otv6 = runge_kutta (10, 0.00001)
otv5 = runge_kutta (10, 0.0001)

otv4 = runge_kutta (10, 0.001)
plt.plot(otv4[0], otv4[1])
otv3 = runge_kutta (10, 0.01)
plt.plot(otv3[0], otv3[1])
otv2 = runge_kutta (10, 0.1)
plt.plot(otv2[0], otv2[1])
plt.show()

for i in range(10):
    print ("ref: {0:+15.10f} {1:+15.10f}".format(otv6[1][i*10**5], otv6[2][i*10**5]))
    print ("2: {0:+20.14f} {1:+20.14f}".format(otv2[1][i*10**1]/otv6[1][i*10**5]-1, otv2[2][i*10**1]/otv6[2][i*10**5]-1))
    print ("3: {0:+20.14f} {1:+20.14f}".format(otv3[1][i*10**2]/otv6[1][i*10**5]-1, otv3[2][i*10**2]/otv6[2][i*10**5]-1))
    print ("4: {0:+20.14f} {1:+20.14f}".format(otv4[1][i*10**3]/otv6[1][i*10**5]-1, otv4[2][i*10**3]/otv6[2][i*10**5]-1))
    print ("5: {0:+20.14f} {1:+20.14f}".format(otv5[1][i*10**4]/otv6[1][i*10**5]-1, otv5[2][i*10**4]/otv6[2][i*10**5]-1))
    print()























