import socket
import string
import sys

s = socket.socket()
port = 9001
if len(sys.argv) > 1:
	host = sys.argv[0]
else:
	host = raw_input("Pleas enter the address of the server:\t")
continue_flag = True

print "**Attempting a connection"
s.connect((host,port))

#Just have one send one receive interface
while continue_flag:
	message =  s.recv(1024)
	print str(message.split('#$%')[0])
	if 'main/bye-bye' in str(message.split('#$%')[1]):
		print "Attempting Exit"
		continue_flag = False
		continue
	while True:
		command = raw_input(str(message.split('#$%')[1]))
		if len(command) > 1:
			break
	s.send(command)