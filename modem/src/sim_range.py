#!/usr/bin/env python
# license removed for brevity
import rospy
import numpy as np
import random
import math
from modem.msg import target, dataMessage
from nav_msgs.msg import Odometry

class modem():
	def __init__(self):
		self.Total = 5
		self.M = np.zeros(self.Total)
		self.T1 = rospy.get_param("~T1_pos",(100,200,0))
		self.T2 = rospy.get_param("~T2_pos",(500,200,0))
		self.T3 = rospy.get_param("~T3_pos",(1000,500,100))
		self.T4 = rospy.get_param("~T4_pos",(0,0,50))
		self.T5 = rospy.get_param("~T5_pos",(50,50,50))
		self.T = [self.T1,self.T2,self.T3,self.T4,self.T5]
		print self.T

# Interprets the Odometry message to find the values of the x,y,z positions
def find_T(msg):
	dat = msg.pose
	dat = str(dat)
	pos = dat[(dat.find('position:')+1):(dat.find('orientation:')-1)]
	x = pos[(pos.find('x')+3):(pos.find('y')-5)]
	y = pos[(pos.find('y')+3):(pos.find('z')-5)]
	z = pos[(pos.find('z')+3):(pos.find('or')-1)]
# and converts the values to floating point values and returns them in an array
	x = float(x)
	y = float(y)
	z = float(z)
	Target = (x,y,z)
	print 'True position is',Target
# and starts the sim range function
	sim_range(Target)

def sim_range(Target):
# Calculates the range to the targeet from the pre-defined transponders and adds a noise
	Noise = 1 #sets the magnatude of the added noise to the distances, I think that this is a relatively ok guess
	#positions of transponders - which is kept as a constant
	T1 = a.T[0]
	T = a.T
	n=len(T1) #determine number of unknowns(dimensions)
	measure = len(T) #determine number of measurments(transponders)
	M = np.zeros((measure))
	M1 = np.zeros((measure,n));
	
	#measurements from target to transponders - saved as a difference in each of the dimensions
	for i in range(0,measure):
		for k in range(0,n):
			M1[i][k] = ((T[i][k]-Target[k])+Noise*random.random())**2
	#print M1
	#store these as a single distance (as opposed as difference in each dimension) per transponder in a single array
	for i in range(0,measure):
		M[i] = math.sqrt(sum(M1[(i)]))
	a.M = M
	#print a.M
	#and sends them to updateRange via sent_T
	for i in range(0,measure):
		send_T(i)

def send_T(n):
# Publishes the simulates ranges as an array to the updateRange topic for the Gausss code
	pubRange = rospy.Publisher("modem/updateRange", dataMessage, queue_size=10)
	pub = dataMessage()
	pub.target = (n+1)
	pub.payload = str(a.M[n])
	#print a.M[n]
	print pub
	pubRange.publish(pub)


rospy.init_node('sim_range', anonymous=True)
# Sets up the modem class and initialises the ros functions to run this as a ros node
a = modem()
subRange = rospy.Subscriber("/uwsim/girona500_odom_RAUVI",Odometry, find_T)
rospy.spin()



