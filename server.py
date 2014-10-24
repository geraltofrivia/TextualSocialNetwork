import socket
import threading
import os

connection_port = 9000
client_port = 10000

def receive(client,addr):
	print "Initiating a receiver"
	while True:
			#Just hold the client here
			msg = client.recv(1024)
			if msg == 'abracadabra':
				print success
			print addr, "says: ", msg

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~MANAGEMENT FUNCTIONS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#Function used to tranfer the socket used by the client
def transfer_connection(client,addr,port):
	#Initialize a socket here now
	connection = socket.socket()
	host = socket.gethostname()
	connection.bind((host,port))
	connection.listen(1)

	#Notify the client about the updated print
	connection port
	client.send(str(port),len(str(port))+1)							#Add 1 to length to solve a minor bug. Client receiving 1000 in place of 10000
	client.close()
	#Wait for the client to connect to the new socket
	client,addr = connection.accept()
	return (client,addr)
	
#This function will create a new thread for the client.
def transfer_control(client,addr):
	#Make a new thread for clients
	thread = threading.Thread(target = receive, args=(client,addr,))
	thread.setDaemon(True)
	thread.start()
	print "THREADING DONE!" 
	return


'''Starting block of our program. 
This block initiates a socket on port 9000 and waits for clients to come.
As soon as they do, we transfer the client into a new thread and push it to login/register modules. 
Hereby we ready the main thread to accept more connections on the socket.'''
#Initialize the socket which accepts connection and binds client to a thread.
connection = socket.socket()
host = socket.gethostname()
port = connection_port
connection.bind((host,port))	
connection.listen(5000)

while True:
	client, addr  = connection.accept()
	print "Got connection from", addr
	#Break into a new thread.
	#Return after login
	#Call the interface/command read function....
	message = "Thank you for connecting to "
	client.send(message, len(message))
	'''Now the client has connected. We would want to transfer this into a new socket 
	and hold the client, while clearing the main socket for more clients'''
	client,addr = transfer_connection(client,addr,client_port)
	thread = transfer_control(client,addr)

