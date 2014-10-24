import socket
import string

s = socket.socket()
port = 9005
host = socket.gethostname()

print "**Attempting a connection"
s.connect((host,port))

#Just have one send one receive interface
while True:
	message =  s.recv(1024)
	print str(message.split('#$%')[0])
	command = raw_input(str(message.split('#$%')[1]))
	s.send(command)



