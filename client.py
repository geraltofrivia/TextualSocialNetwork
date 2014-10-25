import socket
import string

s = socket.socket()
port = 9008
host = socket.gethostname()
continue_flag = True

print "**Attempting a connection"
s.connect((host,port))

#Just have one send one receive interface
while continue_flag:
	message =  s.recv(1024)
	print str(message.split('#$%')[0])
	if 'main/exit' in str(message.split('#$%')[1]):
		print "Attempting Exit"
		continue_flag = False
	command = raw_input(str(message.split('#$%')[1]))
	s.send(command)