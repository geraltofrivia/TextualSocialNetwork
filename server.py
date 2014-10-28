import socket
import threading
import os
import landing

connection_port = 9001

#Initialize the socket which accepts connection and binds client to a thread.
connection = socket.socket()
host = "0.0.0.0"
port = connection_port
connection.bind((host,port))	
connection.listen(5000)

'''To fetch the IP address of the server'''
temporary_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
temporary_socket.connect(("8.8.8.8",80))
address = temporary_socket.getsockname()[0]
temporary_socket.close()


while True:
	print "(Server): Ready to accept a new connection on %s" % address
	client, addr  = connection.accept()
	print addr, "Connected"
	#Now we want to thread to a new branch and continue handling the client there
	server = landing.Welcome(client,addr)
	server.start()