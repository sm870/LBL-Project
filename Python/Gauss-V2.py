import random
import math
import numpy as np


Target = (100, 500, 100) #true position of the vehicle
Noise = 10 #sets the magnatude of the added noise to the distances
#positions of transponders
T1 = 1000,0,0
T2 = 1000,1000,0
T3 = 0,500,0
T4 = 500,500,500
T5 = 300,800,1000
T = [T1,T2,T3,T4,T5]

n=len(T1) #determine number of unknowns(dimensions)
measure = len(T) #determine number of measurments(transponders)
M = np.zeros(measure)
M1 = np.zeros((measure,n));

# measurements from target to transponders
for i in range(0,measure):
	for k in range(0,n):
		M1[i][k] = ((T[i][k]-Target[k])+Noise*random.random())**2

#store these as a single distance per transponder in a single array
for i in range(0,measure):
	M[i] = math.sqrt(sum(M1[i]))

tol = 1 #set a value for the accuracy
maxcycle = 30 #set maximum number of cycles to run for


x = [400,1200,600] #set initial guess for origin - could be anything

xold = x #saves the previous value of x for comparison to the new one

#initialise the lists needed for the Gauss Newton loop
ds = np.zeros((measure,n))
d = np.zeros(measure)
J = np.zeros((measure,n))

for k in range(0,maxcycle): #starts the loop to calculate the approximation of x
 for i in range(0,measure): #loop that calculates the theoretical distance and the Jacobian matrix 
	ds[i,] = abs((np.subtract(T[i],x)))
	Jnum = np.subtract(x,T[i])
	d[i] = math.sqrt(np.sum((ds[i,]**2)))
	J[i,] = np.divide(Jnum,d[i],dtype=float)

 g = np.linalg.pinv(J.transpose()) #calculates the Moore Penrose pseudoinverse of the Jacobian
 
 # Calculate residuals
 r = M-d 

 gt = g.transpose() #calculates the matrix transpose of the pseudoinverse of the Jacobian
 
 rt = r #.transpose() #calculates the matrix transpose of the residuals
 
 xdot = np.dot((gt),(rt)) #calculates the matrix dot product of the transposes of r and g

 x = np.add(xold,xdot) #calculate new approximate position
 print 'x is:' ,x

 err = abs((np.subtract(x,xold))) #calculate error
 error = math.sqrt(np.sum((err**2)))
 print 'with an error of ',error

 if (error <= tol): #if error is less than tolerance break out of loop and display the final value of x
	print 'The Final accurate value of x is:',x,'\nAfter ',cycles,'cycles'
	break
 xold=x #saves the value of x for future loops
 cycles = (k+1) #increments the value that displays the number of cycles the loop has gone through
 
 print 'End of cycle number',cycles
if (cycles==maxcycle): print 'After the maximum (',maxcycle,') number of cycles \nthe error of',error,'is still above the tolerance of ',tol, '\nhowever the final value of X is:\n',x
