import socket
import threading
import os
import landing

connection_port = 9008

#Initialize the socket which accepts connection and binds client to a thread.
connection = socket.socket()
host = socket.gethostname()
port = connection_port
connection.bind((host,port))	
connection.listen(5000)

while True:
	client, addr  = connection.accept()
	print addr, "Connected"
	#Now we want to thread to a new branch and continue handling the client there
	server = landing.Welcome(client,addr)
	server.start()