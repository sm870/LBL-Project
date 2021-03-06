#!/usr/bin/env python
# license removed for brevity
import random
import math
import numpy as np
import rospy
import serial
from modem.msg import target, dataMessage

#Class to setup all the ros commands to the modem driver node to get range data
class modem():
	def __init__(self):
		self.Total = 5
		self.name = [1,2,3,4,5]
		self.M = np.zeros(self.Total)
		self.voltage = np.zeros(self.Total)
		self.savedr = np.zeros(self.Total)
		rospy.init_node('Gauss', anonymous=True)
		self.subRange = rospy.Subscriber("modem/updateRange", dataMessage, self.SaveRange)
		self.T1 = rospy.get_param("~T1_pos",(100,200,0))
		self.T2 = rospy.get_param("~T2_pos",(500,200,0))
		self.T3 = rospy.get_param("~T3_pos",(1000,500,100))
		self.T4 = rospy.get_param("~T4_pos",(0,0,50))
		self.T5 = rospy.get_param("~T5_pos",(50,50,50))
		self.T = [self.T1,self.T2,self.T3,self.T4,self.T5]
		print self.T

	def SaveRange(self,msg):
# Saves the ranges given by the updateRange topic and if all are recieved then runs the Gauss function
		for n in range(0,(self.Total)):
			#print 'n is:',n,
			if (int(self.name[n])) == int(msg.target):
				#print '\nand name is:',self.name[n]
				#print 'saving range from',msg.target
				self.M[n] = msg.payload
				self.savedr[n] = 1
				#print 'savedr', self.savedr
		if np.all(sermod.savedr):
			Gauss()

def Gauss():
# Takes the rranges from all thhe transponders and implements the Gauss Newton algorithm to find an approximation of the true position
	sermod.savedr = np.zeros(sermod.Total)
	#positions of transponders
	T1 = sermod.T[0]
	T = sermod.T
	
	n=len(T1) #determine number of unknowns(dimensions)
	measure = len(T) #determine number of measurments(transponders)
	M = np.zeros(measure)
	M = sermod.M
	#print M
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
		#print 'x is:' ,x
	
		err = abs((np.subtract(x,xold))) #calculate error
		error = math.sqrt(np.sum((err**2)))
		#print 'with an error of ',error
	
		if (error < tol): #if error is less than tolerance break out of loop and publish/display the final value of x
			print 'The Final accurate value of x is:',x,'\nAfter ',cycles,'cycles'
			return
	
		xold=x #saves the value of x for future loops
		cycles = (k+1) #increments the value that displays the number of cycles the loop has gone through
		 
		#print 'End of cycle number',cycles
	if (cycles==maxcycle): print 'After the maximum (',maxcycle,') number of cycles \nthe error of',error,'is still above the tolerance of ',tol, '\nhowever the 		final value of X is:\n',x


#setup the modem class object to get ranges
sermod = modem()
# spin() simply keeps python code from exiting until this node is stopped
rospy.spin()
