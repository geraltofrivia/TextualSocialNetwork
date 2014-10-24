import socket
import threading
import os
import time
from database.db import Datastore

class Welcome(threading.Thread):
	def __init__(self,client,addr):
		threading.Thread.__init__(self)
		self.database = Datastore()
		
		self.client = client
		self.addr = addr
		self.logged_in = False
		self.userid = None
		
	def get_command(self,first_attempt = True):
		'''Receive the client socket, make a new thread and return control to the main program'''
		welcome_instruction = '''Hello, to start using this service, you will have to either login or register yourself.\nPlease proceed by entering 'login' or 'register' to do the same.\nIf at any time you wish to discontinue using the service, please enter 'exit' '''
		
		instruction = '''You are not yet logged in. Enter either 'login' or 'register' to continue, or 'exit' to stop'''
		
		if first_attempt:
			self.client.send(welcome_instruction,len(welcome_instruction))
		else:
			self.client.send(instruction,len(instruction))
		command = self.client.recv(100)
		print command
		return command
	
	def login(self):
		'''In this function, you send the client the instruction to login.
		Then expect a username and then a password'''
		login_instruction = '[SKIP] Login \n'
		userid_instruction = 'Please type in your user id'
		passwd_instruction = 'Please type in your password'
		error_instruction = 'Incorrect userid / password. Please retry'
		success_instruction = '[SKIP] You are now logged in \n'
		
		self.client.send(login_instruction,len(login_instruction)+1)
		while True:
			self.client.send(userid_instruction,len(userid_instruction)+1)
			userid = self.client.recv(100)
			self.client.send(passwd_instruction,len(passwd_instruction)+1)
			password = self.client.recv(100)
			if userid == 'exit' or password == 'exit':
				self.exit()
			if self.database.check_credentials(userid,password):
				print 'User %s has successfully logged in' % userid
				self.client.send(success_instruction,len(success_instruction)+1)
				self.userid = userid
				self.logged_in = True
				return True
			else:
				self.client.send(error_instruction,len(error_instruction)+1)

	def register(self):
		'''In this function we input values from the client and push it on the database,
		in order to register the client as a valid user.'''
		register_instruction = "[SKIP] Register \n"
		userid_instruction = "Please type in a unique user id"
		usernm_instruction = "Please enter a name to be known by"
		gender_instruction = "Please enter 'male', 'female' depending upon your sex"
		passwd_instruction = "Please type in a password. Keep it secret. Keep it safe"
		userid_already_in_use = "This userid already exists. Please select another one"
		success_instruction = '[SKIP] You are now registered \n'
		
		status = -5
		while status < 0:
			self.client.send(register_instruction,len(register_instruction)+1)
			if status <= -1: 
				self.client.send(userid_instruction,len(userid_instruction)+1)
				userid = self.client.recv(100)
			if status <= -2:
				self.client.send(usernm_instruction,len(usernm_instruction)+1)
				usernm = self.client.recv(100)
			if status <= -3:
				self.client.send(gender_instruction,len(gender_instruction)+1)
				gender = self.client.recv(100)
			if status <= -4:
				self.client.send(passwd_instruction,len(passwd_instruction)+1)
				passwd = self.client.recv(100)

			if userid == 'exit' or usernm == 'exit' or gender == 'exit' or passwd == 'exit':
				self.exit()

			if userid == 'cancel' or usernm == 'cancel' or gender == 'cancel' or passwd == 'cancel':
				return

			status = self.database.insert_new_user(userid,usernm,gender,passwd)
			print "(Register:)status: %s" % status

		print "(Welcome:) User %s registered successfully" %userid
		self.client.send(success_instruction,len(success_instruction)+1)
		return

	def suspend(self,timer = 0):
		if timer != 0:
			time.sleep(timer)
			return
		else:
			while True:
				a = None


	def run(self):
		'''Flow will return here once the thread starts. Ask for login or register (input command)/
		Then login/register function called. Have them both interface with the Datastore class.'''
		first_attempt = True
		while not self.logged_in:
			command = self.get_command(first_attempt)
			if command == 'login':
				self.login()
				break
			if command == 'register':
				self.register()
				self.login()
				break
			if command == 'exit':
				self.exit()
				break
			first_attempt = False

		'''The user has logged in.
		As of now, just suspend the user till infinity'''
		self.suspend()

