#!/usr/bin/env python
# license removed for brevity
import rospy
import serial
from modem.msg import target, dataMessage

TOPIC_PING_TARGET = 'modem/ping'
TOPIC_CHANGE_ADDRESS = 'modem/changeSelfAddress'
TOPIC_QUERY_SELF_STATUS = 'modem/querySelfStatus'
TOPIC_QUERY_TARGET_STATUS = 'modem/queryTargetStatus'
TOPIC_SEND_UNICAST = 'modem/sendUnicast'
TOPIC_SEND_BROADCAST = 'modem/sendBroadcast'
TOPIC_UPDATE_STATUS = 'modem/updateStatus'
TOPIC_UPDATE_RANGE = 'modem/updateRange'

class modem():
    def __init__(self):
        
        self.name = 'modem'

        rospy.init_node(self.name, anonymous=True)

        #self.commPort = rospy.get_param('~commPort', "/dev/ttyUSB0") 
        self.printDebug = rospy.get_param('~printDebug', True) 
        self.driver_rate = rospy.get_param('~driverRate', 0.01) 
        self.soundVelocity = rospy.get_param('~soundVelocity', 1500.0) 
        self.driver_loop = rospy.Rate(self.driver_rate)	      
	self.ser = serial.Serial(port="/dev/ttyUSB0",
	                         baudrate=9600,
	                         parity=serial.PARITY_NONE,
	                         stopbits=serial.STOPBITS_ONE,
	                         bytesize=serial.EIGHTBITS)
        
        self.sub_ping_target = rospy.Subscriber(TOPIC_PING_TARGET, target, self.pingTarget, tcp_nodelay=True, queue_size=1)
        self.sub_change_self_address = rospy.Subscriber(TOPIC_CHANGE_ADDRESS, target, self.setSelfAddress, tcp_nodelay=True, queue_size=1)
        self.sub_query_self_status = rospy.Subscriber(TOPIC_QUERY_SELF_STATUS, None, self.querySelfStatus, tcp_nodelay=True, queue_size=1)
        self.sub_query_target_status = rospy.Subscriber(TOPIC_QUERY_TARGET_STATUS, target, self.queryTargetStatus, tcp_nodelay=True, queue_size=1)
        self.sub_send_unicast = rospy.Subscriber(TOPIC_SEND_UNICAST, dataMessage, self.sendUnicastMessage, tcp_nodelay=True, queue_size=1)
        self.sub_send_broadcast = rospy.Subscriber(TOPIC_SEND_BROADCAST, dataMessage, self.sendBroadcastMessage, tcp_nodelay=True, queue_size=1)
        
        self.run()
              
    def pingTarget(self, msg):
        #'''        Pings msg.target        '''
	print 'recieved msg'
        sendThis = '$P%03d' %msg.target
        if self.printDebug: print 'Ping called, sending {0}'.format(sendThis)
        self.ser.write(sendThis)
        
    def setSelfAddress(self, msg):
        #'''        Sets own address to msg.target        '''
        sendThis = '$A%03d'%(msg.target)
        if self.printDebug: 
		print 'Trying to change own address to, {0}'.format(sendThis)
        self.ser.write(sendThis)
        
    def querySelfStatus(self, msg): #Might need a message - does
        #'''        Query own status      '''
        sendThis = '$?'
        if self.printDebug: print 'Querying own status'
        self.ser.write(sendThis)
            
    def queryTargetStatus(self, msg): 
        #'''        Query own status      '''
        sendThis = '$V%03d'%(msg.target)
        if self.printDebug: print 'Querying {0} status'.format(msg.target)
        self.ser.write(sendThis)
        
    def sendUnicastMessage(self, msg): 
        #'''        Sends unicast messsage to msg.target      '''
        sendThis = '$V%03d%01s%s'%(msg.target,(str(len(msg.payload))), msg.payload)
        if self.printDebug: print 'Sending unicast message:', sendThis
        self.ser.write(sendThis)
        
    def sendBroadcastMessage(self, msg): 
        #'''        Sends broadcast messsage     '''
        sendThis = '$B%s%s'%(chr(len(msg.payload)), msg.payload)
        if self.printDebug: print 'Sending broadcast message:', sendThis 
        self.ser.write(sendThis)        
            
    def readMessage(self):
        if self.ser.available():
            line = self.ser.readline()
            if line:
                print line
		if "#A" in line:	
			if "V" in line:
				name = line[(line.find('A')+1):(line.find('A')+4)]
				v = line[(line.find('V')+1):(line.find('V')+5)]
				try:
					voltage = (float(v))*1
					print 'The address of this transponder is',name, 'and the voltage is',voltage
				except:
					print 'could not read voltage of this transponder\nGot',v
			else:
				name = line[(line.find('A')+1):(line.find('A')+4)]
				print 'the node address has been set to',a
			pub = rospy.Publisher(TOPIC_UPDATE_STATUS, dataMessage, queue_size=10)
			publish = dataMessage()
			try:
				publish.payload = v
			except:
				print 'Changing address'
			publish.target = name
			pub.publish(publish)
			
		if "#R" in line:
			if "T" in line:
				const = (6.25*0.00001)*soundVelocity
				read_range = line[(line.find('T')+1):(line.find('T')+6)]
				name = line[(line.find('R')+1):(line.find('T')-1)]
				try:
					x = float(read_range)*const
					print 'The distance to', msg.target, 'is',x
				except: 
					print 'Could not find the distance'
					x ='E'
				pub = rospy.Publisher(TOPIC_UPDATE_RANGE, dataMessage, queue_size=10)
				publish = dataMessage()
				publish.payload = x
				publish.target = name
				pub.publish(publish)
			if "V" in line:
				const = ((6.0/1024.0)*1.1)
				read_voltage = line[(line.find('V')+1):(line.find('V')+5)]
				name = line[(line.find('R')+1):(line.find('V')-1)]
				try:
					v = (int(read_voltage))*const
					print 'The voltage of', msg.target, 'is',v
				except:
					print 'could not read the voltage of transponder', target
					v = 'E'
				pub = rospy.Publisher(TOPIC_UPDATE_STATUS, dataMessage, queue_size=10)
				publish = dataMessage()
				publish.payload = v
				publish.target = name
				pub.publish(publish)
		if "#U" in line:
			a = line[(line.find('U')+1):(line.find('U')+3)]
			if (len(line))==6:
				print 'Data sent successfully to',a
			else:
				data = line[(line.find('U')+1):(line.find('U')+(int(line[line.find('U')+1])+1))]
				print 'Recieved the following',data, 'from',a
		if "#B" in line:
			if (len(line))==3:
				print 'Broadcast sent successfully',line
			else:
				a = line[(line.find('B')+1):(line.find('B')+3)]
				data = line[(line.find('B')+5):(line.find('B')+5+(int(line[line.find('B')+4])))]
				print 'Recieved the following',data, 'from',a

            else:
                print "line is empty"
        
    def run(self):
        while not rospy.is_shutdown():
            self.readMessage()
            try:
                self.driver_loop.sleep()
            except rospy.ROSInterruptException:
                rospy.loginfo('%s shutdown requested ...', self.name)
            
a = modem()
