from socket import *
import socket
import string
import sys

s = socket.socket()
port = 9001
if len(sys.argv) > 1:
	host = sys.argv[1]
	print host
else:
	host = raw_input("Please enter the address of the server:\t")
continue_flag = True

while True:
	try:
		print "**Attempting a connection on", host, ":", port
		s.connect((host,port))
	except socket.error as error:
		if error.errno == 111 or error.errno == 107:
			print "(ERROR): The client is unable to connect to the server. Please ensure that the server is online and you have specified the correct address and port"
			print "(Ping): Enter the correct IP and Port number of the server seperated by a space. Enter exit instead to terminate this application"
			command = raw_input().lower().strip()
			
			if command == "exit":
				exit()

			commands = command.split()
			if len(commands) >= 2 and commands[1].isdigit():
				host = commands[0]
				port = int(commands[1])
			else:
				print "(ERROR): Please enter a valid IP address and port number"
				continue
		
		else:
			break


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