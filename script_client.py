import socket
import string

s = socket.socket()
port = 9006
host = socket.gethostname()

print "**Attempting a connection"
s.connect((host,port))

#Just have one send one receive interface
while True:
	message = s.recv(1024)
	print message
	if message.split()[0] == '[SKIP]':
		continue
	command = raw_input()
	s.send(command)



