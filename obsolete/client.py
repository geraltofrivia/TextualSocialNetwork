import socket
import string

def transfer(port):
	server = socket.socket()
	host = socket.gethostname()
	server.connect((host,string.atoi(port,base = 10)))
	print s.recv(1024)
	s.close()
	return server

s = socket.socket()
port = 9000
host = socket.gethostname()

print "**Attempting a connection"
s.connect((host,port))

print s.recv(1024)
port = s.recv(1024)
print port
server = transfer(port)
msg = ""
while True:
	msg = raw_input()
	server.send(msg,len(msg)+1)
print "Exited"
s.close()

