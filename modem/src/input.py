#!/usr/bin/env python
# license removed for brevity
import rospy
import serial
import numpy as np
from modem.msg import target, dataMessage

class modem():
	def __init__(self):
		self.Total = 5
		self.name = [0,1,2,3,4]
		self.m = np.zeros(self.Total)
		self.voltage = np.zeros(self.Total)
		
		
		rospy.init_node('input', anonymous=True)
		self.pubRange = rospy.Publisher("modem/ping", target, queue_size=10)
		self.pubVoltage = rospy.Publisher("modem/queryTargetStatus", target, queue_size=10)
		self.pubSend = rospy.Publisher("modem/sendUnicast", dataMessage, queue_size=10)
	    	self.subVoltage = rospy.Subscriber("modem/updateStatus", dataMessage, self.SaveVoltage)
		self.subRange = rospy.Subscriber("modem/updateRange", dataMessage, self.SaveRange)
	
	def SaveRange(self,msg):
		#for n in range(0,self.Total):
			#if self.name[n] == msg.target:
				#self.m[n] = msg.payload
		print msg

	def SaveVoltage(self,msg):
		for n in range(0,self.Total):
			if self.name[n] == msg.target:
				self.voltage[n] = msg.payload
	
	def GetRange(self,to):	
		#for n in range(0,self.Total):
		#print to		
		to = int(to)
		Target = target()		
		Target = self.name[to]
		self.pubRange.publish(Target)
		print 'published, hopefully'

	def GetVoltage(self):
		for n in range(0, self.Total):
			Target = target()
			Target.target = self.name[n]
			self.pubVoltage.publish(Target)

	def SendData(self,data, address):
		publish = dataMessage()
		publish.payload = data
		publish.target = address
		self.pubSend.publish(publish)
	
def input_pub():
	a = modem()	

	print 'Input command:'
	string = str(raw_input())
	if string == 'ping':
		print 'Enter target:'
		to = input()
		to = int(to)
		#print to
		a.GetRange(to)
		#print a.m
	if string == 'voltage':
		a.GetVoltage()
		print a.voltage
	if string == 'send':	
		print 'What do you want to send?'
		data = raw_input()
		print 'To where?'
		address = raw_input()
		a.SendData(data, address)
	input_pub()	
	rospy.spin()

if __name__ == '__main__':
    try:
        input_pub()
    except rospy.ROSInterruptException:
        pass
