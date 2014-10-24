import socket
import threading
import os
import landing

connection_port = 9006

#Initialize the socket which accepts connection and binds client to a thread.
connection = socket.socket()
host = socket.gethostname()
port = connection_port
connection.bind((host,port))	
connection.listen(5000)

while True:
	client, addr  = connection.accept()
	print "Got connection from", addr
	server = landing.Welcome(client,addr)
	server.run()
	'''#Break into a new thread.
	#Return after login
	#Call the interface/command read function....
	message = "Thank you for connecting to "
	client.send(message, len(message))
	client,addr = transfer_connection(client,addr,client_port)
	thread = transfer_control(client,addr)'''