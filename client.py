from socket import *
import socket
import string
import sys
import time

s = socket.socket()
port = 9000
if len(sys.argv) > 1:
	host = sys.argv[1].split(':')[0]
	print host

	if len(sys.argv[1].split(':')) > 1:
		port = sys.argv[1].split(':')[1]
	elif len(sys.argv) > 2:
		port = sys.argv[2]
	
else:
	host = raw_input("(Ping): Please enter the IP address of the server: ")
	port = raw_input("(Ping): Please enter the Port number of the server: ")
	
while True:
	try:
		port  = int(port)
	except ValueError:
		port = raw_input("(Error): The port number you entered does not look like a valid number. Please enter it again")
		if port.isdigit():
			port = int(port)
		break	
	else:
		break

continue_flag = True

while True:
	try:
		print "**Attempting a connection on", host, ":", port
		s.connect((host,port))
	except socket.error as error:
		if error.errno == 111 or error.errno == 107:
			print "(Error): The client is unable to connect to the server. Please ensure that the server is online and you have specified the correct address and port"
			command = raw_input("(Ping): Enter the correct IP and Port number of the server seperated by a space. Enter exit instead to terminate this application: ").lower().strip()
			
			if command == "exit":
				exit()

			commands = command.split()
			if len(commands) >= 2 and commands[1].isdigit():
				host = commands[0]
				port = int(commands[1])
			else:
				print "(Error): Please enter a valid IP address and port number"
				continue
		else:
			break
	else:
		break



#Just have one send one receive interface
while continue_flag:
	message =  s.recv(1024)
	message_ = str(message.split('#$!')[0])
	prompt_ = str(message.split('#$!')[1])
	
	
	#Routine for client exit
	if 'main/bye-bye' in prompt_:
		print "Attempting Exit"
		continue_flag = False
		continue

	#Routine for long message detection
	if prompt_.lower().strip() == 'incoming':
		print "Long message incoming. Please wait while we proceed to fetch it all for you"
		n = int(message_.strip())
		messages = []
		s.send("Ready!")
		for i in range(n):
			messages.append(s.recv(1024))
			print "Receiving Block" ,i
			time.sleep(1)
			s.send("OK")
		#assuming that the trailing part of last message has some prompt, we extract it.
		message_ = ''.join( s for s in messages)
		prompt_ = str(message_.split('#$!')[-1])


	print message_
	while True:
		command = raw_input(prompt_)
		if len(command) > 1:
			break
	s.send(command)