#!/usr/bin/env python
# license removed for brevity
import random
import math
import numpy as np
import rospy
import serial
import time
from modem.msg import target, dataMessage
from nav_msgs.msg import Odometry

#Class to setup all the ros commands to the Gauss code to find the postion of the vehicle and save it and all the variables needed in many functions
class modem():
	def __init__(self):
		self.pubPos = rospy.Publisher("modem/savePos", target, queue_size=10)
		self.subing = rospy.Subscriber("modem/savePos", target, printing)
		self.subPos = rospy.Subscriber("modem/updatePos", dataMessage, pos)
		# The next topic is not the correct topic or message type, it should be to set the vehicles velocity
		self.pubVelocity = rospy.Publisher("/uwsim/setVehicleVelocity", dataMessage, queue_size=10)
		rospy.init_node('Nav', anonymous=True)
		self.pos = np.zeros(3)
		self.i = 0
		self.flag = 1

def printing(msg):
# Debug function to check if the message published to the ros topic correctly
	print 'got the message:',msg

def trig(pos,desired_pos):
# Implements the mathematics required to convert the positions into a vector for the vehicle to travel
	pos1 = pos
	pos2 = desired_pos
	print 'pos 1 is:',pos1,'pos 2 is:',pos2
	velocity = np.zeros(3)
	diffx = pos2[0]-pos1[0]
	diffy = pos2[1]-pos1[1]
	diffz = pos2[2]-pos1[2]
	diff = np.array([diffx,diffy,diffz])
	magdiff = np.sqrt(diff.dot(diff))
	#to find unit vector, divide by magnatude
	velocity[0] = diff[0]/magdiff
	velocity[1] = diff[1]/magdiff
	velocity[2] = diff[2]/magdiff
	time = magdiff
	print 'velocity is:',velocity,'and time is:',time
	return velocity,magdiff

def pos(msg):
# Saves the message's payload as a position on an axis (x,y,z) and once all of these is found then run the Move code
	print msg
	if msg.target == 0:
		an.pos[0] = float(msg.payload)
	if msg.target == 1:
		an.pos[1] = float(msg.payload)
	if msg.target == 2:
		an.pos[2] = float(msg.payload)	
	pos = Move()
	print pos

def Move():
# Code that runs the navigation of the vehicle,
# recieving the position of the vehicle and taking the next position in the loop then running the trig function
# to find a unit vector (so the vehicle always moves at a speed of 1) and a time then seting the velocity of the
# vehicle and waiting the required time and then setting the velocity to zero again, this repeates for each value of the 
# positions.
	next_pos=[[1.,2.,-3.],[2.,3.,-4.],[10.,10.,-5.],[1.,10.,-2.],[1.,2.,-2.]]
	b = trig(an.pos,next_pos[an.i])
	an.velocity = b[0]
	an.time = b[1]
# Code that should set the velocity of the vehicle but currently is just dummy code that will run
	publish = dataMessage()
	publish.payload = str(an.velocity[0])
	publish.target = 0
	an.pubVelocity.publish(publish)
	publish.payload = str(an.velocity[1])
	publish.target = 1
	an.pubVelocity.publish(publish)
	publish.payload = str(an.velocity[2])
	publish.target = 2
	an.pubVelocity.publish(publish)
######################################################################
	time.sleep(an.time)
######################################################################
	publish.payload = str(0)
	publish.target = 0
	an.pubVelocity.publish(publish)
	publish.payload = str(0)
	publish.target = 1
	an.pubVelocity.publish(publish)
	publish.payload = str(0)
	publish.target = 2
	an.pubVelocity.publish(publish)
######################################################################
	#print 'i is:',an.i,'\nand its max shoulb be:',(len(next_pos))
	if an.i != (len(next_pos)-1):
		an.pubPos.publish(1)
		an.i += 1
		return
	else:
		an.pubPos.publish(1)
		an.i = 0
		return 'Done'

# Sets the modem class
an = modem()
# Initial request for position, starts the loop but only runs once
if an.flag == 1:
	print 'publishing the starting request for position' 
	an.pubPos.publish(2)
	print 'published'
	an.flag = 0
# spin() simply keeps python code from exiting until this node is stopped
rospy.spin()
