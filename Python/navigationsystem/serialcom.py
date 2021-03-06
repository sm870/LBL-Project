c = 340
import serial

def ranges(com,address,total):
	n = total
	m = [0,]*n
	com = str(com)
	for i in range(0,n):
		target = '000'
		target += str(i)
		target = target[-3:]
		if (target != address):
			m[i] = distance(target,com)
	return m

def battcheck(com,address,total):
	lowV = 0
	const = ((6.0/1024.0)*1.1)
	n = total	
	com = str(com)
	v = [0,]*n
	for i in range(0,n):
		target = '000'
		target += str(i)
		target = target[-3:]
		if(target != address):
			v[i] = checkV(target,com)
			if (v[i] <= lowV):
				print 'replace battery in transponder',i
		else:
			status = status(com)
			read_voltage = status[(status.find('V')+1):(status.find('V')+5)]
			try:
				v[i] = (float(read_voltage))*const
			except:
				print 'could not read voltage of this transponder'
				v[i] = 'E'
			if (v[i] <= lowV):
				print 'replace battery in transponder',i
	return v

def ping(target,commport):
	ser = serial.Serial(commport,timeout = 2)
	print 'ok, pining transponder',target
	string = '$P'
	string += str(target)
	print 'command string is',string
	ser.write(string)
	read = ser.read(20)
	ser.close()	
	return read

def distance(target,commport):
	ser = serial.Serial(commport,timeout = 2)
	const = 6.25*0.00001*c
	#print 'ok, pining transponder',target
	string = '$P'
	string += str(target)
	#print 'command string is',string
	ser.write(string)
	read = ser.read(20)
	print read
	read_range = read[(read.find('T')+1):(read.find('T')+6)]
	try:
		x = float(read_range)*const
	except: 
		print ' no range read'
		return 'E'		
	ser.close()
	return x

def status(commport):
	ser = serial.Serial(commport,timeout = 2)
	print 'ok, finding the status of this transponder'
	ser.write(b'$?')
	read = ser.read(20)
	ser.close()
	return read

def checkV(target,commport):
	ser = serial.Serial(commport,timeout = 2)
	print 'ok, finding the voltage of transponder',target
	string = '$V'
	string += str(target)
	print 'command string is',string
	ser.write(string)
	read = ser.read(20)
	print read
	read_voltage = read[(read.find('V')+1):(read.find('V')+5)]
	try:
		v = (int(read_voltage))*const
	except:
		print 'could not read the voltage of transponder', target
		return 'E'
	ser.close()
	return v

def broadcast(commport,data):
	ser = serial.Serial(commport,timeout = 2)
	print 'ok, broadcasting to all transponders'
	string = '$B'
	string += len(data)
	string += str(data)
	print 'command string is',string
	ser.write(string)
	read = ser.read(20)
	return read
