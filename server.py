import socket
import threading
import os
import landing

connection_port = 9001

#Initialize the socket which accepts connection and binds client to a thread.
connection = socket.socket()
host = "0.0.0.0"
port = connection_port
#Try to bind the socket to the given port. Otherwise switch to the next working port
while True:
	try: 
		connection.bind((host,port))
	except socket.error as error:
		if error.errno == 98:
			print "(ERROR): Port", port,"already in use. Running the server on port", port + 1, "instead"
			port += 1
		else:
			break
connection.listen(5000)

#To fetch the IP address of the server, we try and instantiate a connection to a dummy ip and port, only to fetch the IP of this computer
temporary_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
	temporary_socket.connect(("8.8.8.8",80))
	address = temporary_socket.getsockname()[0]
except socket.error as error:
	if error.errno == 101:
		print "(WARNING): Server offline. Only local clients can connect."
		address = "127.0.0.1"
	else:
		address = temporary_socket.getsockname()[0]
temporary_socket.close()


while True:
	print "(Server): Ready to accept a new connection on %s" % address +' : '+ str(connection.getsockname()[1])
	client, addr  = connection.accept()
	print addr, "Connected"
	#Now we want to thread to a new branch and continue handling the client there
	thread = landing.Welcome(client,addr)
	thread.start()
