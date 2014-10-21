import socket
import threading
import os


#Initialize the socket which accepts connection and bind"s client to a thread.
connection = socket.socket()
host = socket.gethostname()
port = 9500
connection.bind((host,port))


#Function used to tranfer the socket used by the client
def transfer_connection(client,addr,port):
	#Initialize a socket here now
	connection = socket.socket()
	host = socket.gethostname()
	connection.bind((host,port))
	connection.listen(1)

	#Notify the client about the updated connection
	client.send(str(port),len(str(port)))
	client.close
		
	#Wait for the client to connect to the new socket
	client,addr = connection.accept()
	return (client,addr)


def receive(client,addr):
	print "Initiating a receiver"
	while True:
			#Just hold the client here
			print addr, "says: ", client.recv(1024)

	
#This function will create a new thread for the client.
def transfer_control(client,addr,counter):
	#Make a new thread for clients
	thread = threading.Thread(target = receive, args=(client,addr,))
	thread.setDaemon(True)
	thread.start()
	print "THREADING DONE!" 
	return
	


#The thread class. This will hold the client connections on unique sockets
class mythread (threading.Thread):
	def __init__(self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter
	def run(self,client,addr):
		print "Starting new thread for ", addr
		client.send("Thank you for shifting connection. You can now initiate your chat")
		

connection.listen(5)
counter = 0


while True:
	client, addr  = connection.accept()
	counter = counter + 1				
	print "Got connection from", addr
	message = "Thank you for connecting."
	client.send(message, len(message))
	
	#Now the client has connected. We would want to transfer this into a new socket and hold the client, while clearing the main socket for more clients
	client,addr = transfer_connection(client,addr,port+counter)
	thread = transfer_control(client,addr,counter)
