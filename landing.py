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
		self.buffer = ''
		
	def send(self,message,prompt = 'main',length = 1024,buffer = False):
		'''This function is used to implement a prompt on the client side.
		It masks client.send.	We now follow a (send,send,receive) UX. The second send is solely for the prompt
		prompt - The value that denotes where the client ought to be when he next types in a command
		length -  The length of text to receive from the client
		buffer - If buffer is true, we don't want to send the message just yet.
							We want to store it somewhere and send it off with the next send.
							The situation will arise when the server will have something to say but nothing to receive
							The reason for this is the (send,recv) UX we setup'''

		if buffer:
			self.buffer = self.buffer + '\n' + message
			return
		if self.logged_in:
			prompt = self.userid + '@' + prompt
		prompt = prompt + ':$ '
		if len(self.buffer) > 0:
			message = self.buffer + '\n' + message
			self.buffer = ''
		message = message + '#$%' + prompt
		self.client.send(message)
		return self.client.recv(length)
		
	def get_instruction(self,first_attempt = True,independent = True):
		'''Receive the client socket, make a new thread and return control to the main program'''
		welcome_instruction = '''Hello, to start using this service, you will have to either login or register yourself.\nPlease proceed by entering 'login' or 'register' to do the same.\nIf at any time you wish to discontinue using the service, please enter 'exit' '''
		error_instruction = '''You are not yet logged in. Enter either 'login' or 'register' to continue, or 'exit' to stop'''
		further_instruction = '''What do you want to do now?'''

		if not self.logged_in:
			if first_attempt:
				command = self.send(welcome_instruction,'main',100)
			else:
				command = self.send(error_instruction,'main',100)
			return command
		else:
			command = self.send(further_instruction,'main',100)
			return command
		
	def login(self):
		'''In this function, you send the client the instruction to login.
		Then expect a username and then a password'''
		userid_instruction = 'Please type in your user id'
		passwd_instruction = 'Please type in your password'
		error_instruction = 'Incorrect userid / password. Please retry'
		success_instruction = 'You are now logged in'
		
		#self.client.send(login_instruction,len(login_instruction)+1)
		while True:
			userid = self.send(userid_instruction,'login',100)
			password = self.send(passwd_instruction,'login',100)
			
			if userid == 'exit' or password == 'exit':
				self.exit()
			if self.database.check_credentials(userid,password):
				print self.addr,'User %s has successfully logged in' % userid
				self.send(success_instruction,buffer = True)
				self.userid = userid
				self.logged_in = True
				return True

	def register(self):
		'''In this function we input values from the client and push it on the database,
		in order to register the client as a valid user.'''
		register_instruction = "[SKIP] Register \n"
		userid_instruction = "Please type in a unique user id"
		usernm_instruction = "Please enter a name to be known by"
		gender_instruction = "Please enter 'male', 'female' depending upon your sex"
		passwd_instruction = "Please type in a password. Keep it secret. Keep it safe"
		success_instruction = '[SKIP] You are now registered \n'
		
		status = -5
		while status < 0:
			#self.client.send(register_instruction,len(register_instruction)+1)
			if status <= -1: 
				userid = self.send(userid_instruction,'register',100)
			if status <= -2:
				usernm = self.send(usernm_instruction,'register',100)
			if status <= -3:
				gender = self.send(gender_instruction,'register',100)
			if status <= -4:
				passwd = self.send(passwd_instruction,'register',100)

			if userid == 'exit' or usernm == 'exit' or gender == 'exit' or passwd == 'exit':
				self.exit()

			if userid == 'cancel' or usernm == 'cancel' or gender == 'cancel' or passwd == 'cancel':
				return False

			status = self.database.insert_new_user(userid,usernm,gender,passwd)

		print self.addr,"User %s registered successfully" %userid
		self.send(success_instruction,buffer = True)
		return True

	def help(self,operation = None,independent = True):
		'''This function is used to provide the user with all the things that he can do with the system.
		 List of all the functions and their description is to be given to the client.
		 Further, description of one single function can also be extracted using independent and operation args'''

		instruction = '''To interact with the system, you will have to type in commands.\nAt any point of time, you can type in 'exit' to exit the system, and 'cancel' to cancel that operation\n'''
		description = []
		description.append(('post','\t\tTo post content on the netork. It will be seen by the people who have subscribed to you\n'))		
		description.append(('poke','\t\tTo send a poke to a specific user\n'))
		description.append(('timeline','\tTo view the posts of users you have subscribed to\n'))
		description.append(('up','\t\tTo support/like a post. You can only like a post once\n'))
		description.append(('users','\t\tTo view a list of all the users in the database\n'))
		
		if operation == None:
			message = instruction
			for command in description:
				message = message+command[0]+str(command[1])
			message = message

		else:
			message = ''
			for command in description:
				if command[0] == operation:
					message = message+command[0]+str(command[1])
			if independent:
				message = message

		self.send(message,buffer = True)
		
	def users(self,skip_subscribed = False):
		'''This function will be used to display a list of all the users registered in the database
		At a go, it will only display a certain number of users before confirming to continue further'''
		users = self.database.get_all_users()
		if skip_subscribed:
			subscribed = self.database.get_subscriptions_of(self.userid)

		message = ''
		for user in users:
			if skip_subscribed == True:
				if user[0] in subscribed:
					continue
			if not user[0] == self.userid:
				message = message + user[0] + '\t\t' + user[1] + '\n'
		self.send(message,buffer = True)
		return

	def post(self):
		'''In this function, the client will generate a post 
		which will then be shown to timelines of people.
		Since he has already logged in, we won't ask for his userid. 
		We will generate a postid automatically and the only input thus required is the text itself''' 
		content_instruction = '''Please enter the text you want to post'''
		empty_content_instruction = '''We're sorry but you need to enter some content to post'''

		status = -3
		while status < 0:
			content = self.send(content_instruction,'main/post')
		
			if content == 'exit':
				self.exit()
			if content == 'cancel':
				return False

			status = self.database.insert_new_post(self.userid,content)
			#print self.addr,"(Post:)status: %s" % status

		print self.addr,"User %s just posted something" %self.userid
		return True

	def timeline(self, size = 10):
		'''Here we will display all the posts that ought to be displayed to every user.
		The posts will be fetched from the users whom self.user has subscribed to.
		Not all the posts will be shown in one go. Instead, we'll go 10 at a time(by default)
		Format to print a post is " %(userid)s: %(content)s\n\t%+(ups)d, %(timestamp)s, #%(postid)d\n\n" '''
		next_instruction = '''Enter 'next' to see next batch of posts'''
		empty_instruction = '''It seems that your timeline is empty. Why not subscribe to other users to view their posts on your timeline?\nYou know, keep up with your friends\n'''

		counter = 0
		message = ''
		posts = self.database.get_posts_for(self.userid,get_ups = True)

		if len(posts) < 1:
			self.send(empty_instruction, buffer = True)

		for post in posts:
			message = message + post[2] + ': ' + post[1] + '\n   +' + str(post[4]) + ' @' + post[3][:-7] + ' #' + str(post[0]) + '\n\n'
			counter = counter + 1
			if counter >= size:
				message = message + next_instruction
				command = self.send(message,'main/timeline',100)

				message = ''
				counter = 0

				if command == 'exit':
					self.exit()
				if command == 'cancel':
					return False
				if command == 'up':
					self.up(True)

		if len(message) > 0:
			self.send(message, buffer = True)
		return True

	def subscribe(self):
		'''This function will be used to subscribe to other users.
		We expect the client to specify the userid and not usernames (to prevent duplication)'''
		subsid_instruction = '''Please enter the userid of the user you want to subscribe to'''
		error_subsid_instruction = '''The entered user does not exist. Please enter a valid username.\nYou may want to run 'users' to fetch the list of registered users'''
		success_instruction = '''You have successfully subscribed to the user. Your timeline will now contain all his/her posts'''
		
		status = -3
		while status < 0:
			subsid = self.send(subsid_instruction,'main/subscribe',100)

			if subsid == 'exit':
				self.exit()
			if subsid == 'cancel':
				return False
			if subsid == 'users':
				self.users(True)
				continue

			status = self.database.insert_new_subscription(self.userid,subsid)
			if status == -2:
				self.send(error_subsid_instruction,buffer = True)

		print self.addr,"User %s subscribed to another user" %self.userid
		self.send(success_instruction,buffer = True)
		return True

	def up(self, from_timeline = False):
		'''This function will be used to 'up' a post
		We expect the user to know the postid, which can be seen from the timeline'''
		up_instruction = '''Please enter the post id of the post you want to 'up' '''
		error_instruction = '''It seems that the postid you entered does not exist. Kindly recheck the enter'''

		status = -3
		if from_timeline:
			prompt = 'main/timeline/up'
		else:
			prompt = 'main/up'
		while status <0:
			postid = self.send(up_instruction,prompt,20)

			if postid == 'exit':
				self.exit()
			if postid == 'cancel':
				return False

			status = self.database.insert_new_up(postid,self.userid)
			if status == -1:
				self.send(error_instruction,buffer=True)


	def suspend(self,timer = 0):
		print self.addr, "User %s is suspending" % self.userid
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
			command = self.get_instruction(first_attempt)
			if command == 'login':
				self.login()
				break
			if command == 'register':
				self.register()
				self.login()
			if command == 'exit':
				self.exit()
			first_attempt = False

		'''The user has logged in.
		On any call to run(), the function will start from here if the user has logged in. 
		So, the 'cancel' command works just fine by sending calling this function again'''

		first_attempt = False
		self.help()
		while True:
			command = self.get_instruction()
			if command == 'post':
				self.post()
			if command == 'users':
				self.users()
			if command == 'timeline':
				self.timeline()
			if command == 'subscribe':
				self.subscribe()
			if command == 'up':
				self.up()
			if command == 'suspend':
				self.suspend()
			if command == 'help':
				self.help()


