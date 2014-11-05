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
		self.first_attempt = True
		self.need_help = True
		
		self.userid = None
		self.logged_in = False

		self.discontinue = False
		
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
		if self.discontinue:
			return 
		return self.client.recv(length).lower().strip()
		
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
				return self.exit()
			if self.database.check_credentials(userid,password):
				print self.addr,'User %s has successfully logged in' % userid
				self.send(success_instruction,buffer = True)
				self.userid = userid
				self.logged_in = True
				self.need_help = True
				return True
			else:
				self.send(error_instruction,buffer = True)

	def logout(self):
		'''In this function we throw the user out of the logged in state.
		And reset the variables appropriately'''
		success_instruction = '''You have now logged out of the system.'''
		
		self.userd = None
		self.logged_in = False

		print self.addr, "User %s is exiting" % self.userid
		self.send(success_instruction,buffer = True)
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
				return self.exit()

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
		description.append(('ping','\t\tTo send a ping to a specific user\n'))
		description.append(('pings','\t\tTo view all the pings sent to you\n'))
		description.append(('subscribe','\tTo subscribe to a users post.\n'))
		description.append(('timeline','\tTo view the posts of users you have subscribed to\n'))
		description.append(('up','\t\tTo support/like a post.\n'))
		description.append(('users','\t\tTo view a list of all the users in the database\n'))
		description.append(('view','\t\tTo view a users profile page.\n'))
		description.append(('settings','\tTo change settings of your profile\n'))
		description.append(('logout','\t\tTo log yourself out of the system\n'))
		description.append(('exit','\t\tTo exit out of the application.\n'))

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
			#if not user[-1].lower() == 'true':
			#	continue
			if not user[0] == self.userid:
				message = message + user[0] + '\t\t' + user[1] + '\n'
		self.send(message,buffer = True)
		return

	def pings(self,size = 20):
		'''This function will fetch all of the pings that are pointed to the client.
		From within the function, he can ping some user as well'''
		next_instruction = '''Enter 'next' to see next batch of pings'''
		empty_instruction = '''It seems that you have not yet been pinged by any user. Why not initiate it yourself?\nEnter 'ping' to ping any user'''

		counter = 0
		message = ''
		pings = self.database.get_pings_for(self.userid)

		if len(pings) < 1:
			self.send(empty_instruction, buffer = True)

		for ping in pings:
			message = message + ping + '\n'
			counter = counter + 1
			if counter >= size:
				message = message + '\n' + next_instruction
				command = self.send(message,'main/pings',100)

				message = ''
				counter = 0
				
				if command == 'exit':
					return self.exit()
				if command == 'cancel':
					return False
				if command == 'ping':
					self.ping(True)

		if len(message) > 0:
			self.send(message, buffer = True)
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
					return self.exit()
				if command == 'cancel':
					return False
				if command == 'up':
					self.up(True)

		if len(message) > 0:
			self.send(message, buffer = True)
		return True

	def view(self,view_self = False):
		'''This function is used to view a person's profile. There are two states in the function
		View self profile - your posts, your data, the posts you liked, people you've pinged and people who have pinged you
		View others profile - their posts, their data, their pings to you and your pings to them (pings are private)
		If a person types their userid in the main commandline, this function will be called with no arguments
		If a person types view, then the arguments will be fetched by this person will be userid'''
		next_instruction = '''Now, you can choose to view more data of the user. Simply type in the any of the following command that you want to see\n'Posts','Pings',Subscribers','Subscriptions','Ups' '''
		userid_instruction = 'Please enter the userid of the person whose profile you want to see'
		error_userid_instruction = 'This userid does not exist. Please recheck'
		empty_posts = 'This user has not posted anything yet'
		empty_ups = 'This user has not given an up to any post'
		empty_subscribers = 'This user has no subscribers yet'
		empty_subscriptions = 'The user has not subscribed to anyone yet'
		empty_pings_from = 'The user has not been pinged by anyone yet'
		empty_pings_to = 'The user has not pinged anyone yet'
		empty_mentions = "The user has not  been mentioned in anyone's posts yet"

		if view_self:
			userid = self.userid
		else:
			userid = -1

		while userid == -1:
			userid = self.send(userid_instruction,'main/view',100)
			
			if userid == 'exit':
				return self.exit()
			if userid == 'cancel':
				return

			userid = self.database.is_existing_userid(userid)
			if userid == -1:
				self.send(error_userid_instruction,buffer = True)

		#We now have a valid userid
		user_data = self.database.get_user_data(userid)
		posts = self.database.get_posts_of(userid,get_ups =True)
		ups = self.database.get_ups_of(userid,get_ups = True)
		subscribed_to = self.database.get_subscriptions_of(userid)
		subscribers = self.database.get_subscribers_of(userid)
		pings_to_others = self.database.get_pings_by(userid)
		pings_from_others = self.database.get_pings_for(userid)

		message = ''
		counter = 0

		message = user_data[0] + '\nname-' + user_data[1] + '\n' + user_data[2]
		message = message + ', Subscribers: #' + str(len(subscribers)) + ', Subscriptions: #' + str(len(subscribed_to)) + '\n'
		message = message + 'Pings: \tsent: #' + str(len(pings_to_others)) + ', received: #' + str(len(pings_from_others)) + '\n\n'
	
		message = message + 'Recent Posts by ' + userid.upper() +': \n'
		if len(posts) < 1:
			message = message + empty_posts + '\n\n'
		for post in posts:
			message = message + '   ' + post[2] + ': ' + post[1] + '\n\t+' + str(post[4]) + ' @' + post[3][:-7] + ' #' + str(post[0]) + '\n'
			counter = counter + 1
			if counter >= 5:
				break

		message = message + '\nRecent Ups by ' + userid.upper() +': \n'
		if len(ups) < 1:
			message = message + empty_ups + '\n\n'
		counter = 0
		for post in ups:
			message = message + '   ' + post[2] + ': ' + post[1] + '\n'
			counter = counter + 1
			if counter >= 2:
				break		

		self.send(message,buffer = True)
		message = ''
		
		#Take further commands

		while True:
			command = self.send(next_instruction,'main/view',100)

			if command == 'exit':
				return self.exit()
			if command == 'clear' or command == 'back':
				return False
			if command == 'posts':
				message = 'Recent Posts by ' + userid +': \n'
				if len(posts) < 1:
					message = message + empty_posts + '\n\n'
				for post in posts:
					message = message + '   ' + post[2] + ': ' + post[1] + '\n\t+' + str(post[4]) + ' @' + post[3][:-7] + ' #' + str(post[0]) + '\n'
				self.send(message,buffer = True)
				message = ''
				continue
			if command == 'ups':
				message = 'Recent Ups by ' + userid +': \n'
				if len(ups) < 1:
					message = message + empty_ups + '\n\n'
				for post in ups:
					message = message + '   ' + post[2] + ': ' + post[1] + '\n\t+' + str(post[4]) + ' @' + post[3][:-7] + ' #' + str(post[0]) + '\n'
				self.send(message,buffer = True)
				message = ''
				continue
			if command == 'subscribers':
				message = 'Subscribers of '  + userid +': '
				counter = 0
				if len(subscribers) == 0:
					message = message + empty_subscribers
				for user in subscribers:
					message = message + str(user[0]) + ', '
					counter = counter + 1
					if counter >= 10:
						message = message + '\n\t'
						counter = 0
				message = message + '\n'
				self.send(message,buffer = True)
				message = ''
				continue
			if command == 'subscriptions':
				message = 'Subscription of ' + userid + ': '
				counter = 0
				if len(subscribed_to) == 0:
					message = message + empty_subscriptions
				for user in subscribed_to:
					message = message + user + ', '
					counter = counter + 1
					if counter >= 10:
						message = message + '\n\t'
						counter = 0
				message = message + '\n'
				self.send(message,buffer = True)
				message = ''
				continue
			if command == 'pings':
				message = 'Pings For ' + userid + ': '
				counter = 0
				if len(pings_from_others) == 0:
					message = message + empty_pings_from
				for user in pings_from_others:
					message = message + user + ', '
					counter = counter + 1
					if counter >= 10:
						message = message + '\n\t'
						counter = 0
				message = message + '\n'
				message = message + 'Pings To ' + userid + ': '
				counter = 0
				if len(pings_to_others) == 0:
					message = message + empty_pings_to
				for user in pings_to_others:
					message = message + user + ', '
					counter = counter + 1
					if counter >= 10:
						message = message + '\n\t'
						counter = 0
				message = message + '\n'
				self.send(message,buffer = True)
				message = ''
				continue



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
				return self.exit()
			if content == 'cancel':
				return False

			status = self.database.insert_new_post(self.userid,content)
			#print self.addr,"(Post:)status: %s" % status

		print self.addr,"User %s just posted something" %self.userid
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

	def ping(self, from_pings = False):
		'''This function will enable the user to send pings to other users.
		We will assume that the user knows the id of the other userid_instruction
		The parameter is an indication in the prompt regarding where he/she will return to after this operation'''
		ping_instruction = '''Please enter the userid of the person you wish to ping'''
		error_instruction = '''It seems that the userid was incorrect. The user doesn't exist. Kindly recheck and enter'''
		success_instruction = '''The user was successfully pinged. Expect a ping back once he logs in :smile: '''

		status = -3
		if from_pings:
			prompt = 'main/pings/ping'
		else:
			prompt = 'main/ping'

		while status < 0:
			toid = self.send(ping_instruction,prompt,20)

			if toid == 'exit':
				return self.exit()
			if toid == 'cancel':
				return False

			status = self.database.insert_new_ping(self.userid,toid)
			if status == -1:
				self.send(error_instruction,buffer = True)

		self.send(success_instruction,buffer = True)

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
				return self.exit()
			if postid == 'cancel':
				return False

			status = self.database.insert_new_up(postid,self.userid)
			if status == -1:
				self.send(error_instruction,buffer=True)

	def settings(self):
		'''In this function we will show user his preferences and 
		allow him to edit them as per required'''
		welcome_instruction = 'You can change the following settings for your profile. Please enter the command corresponding to any option \n'
		error_instruction = 'Command unrecognized. Please enter a valid command'
		error_visible = 'Please enter either "true" or "false"'
		visible_instruction = 'Enter "true" if you want your profile to be open to be seen by anyone on Ping. \nEnter "false" to hide yourself from global list of users and details of your profile to be viewed from anyone else except for your subscribers'
		options = []
		options.append('Visibility-\tvisible')
		options.append('Change Passoword-\tchange password')
		options.append('Remove my posts-\tremove posts')
		options.append('Remove my subscriptions-\tremove subscriptions')

		instruction = welcome_instruction
		for option in options:
			instruction += '\t' + option + '\n'

		status = -1
		while status <0:
			command = self.send(instruction,'main/settings',100)
			
			if command == 'exit':
				return self.exit()
			if command == 'cancel'or command == 'back':
				return False

			if command == 'visible':
				command_ = self.send(visible_instruction,'main/settings/visible',100)
				status = self.database.update_user_visible(self.userid,command_)
				if status == -2:
					self.send(error_visible,buffer = True)

		

	def exit(self):
		'''This function is used to finally end the client connection'''
		exit_message = 'Closing the connection'
		warning_instruction = 'Are you sure you want to exit? \nPress Yes to continue, No to cancel'

		command = self.send(warning_instruction,'main/exit',100)

		if command == 'exit':
			self.exit()
		if command == 'cancel' or command == 'no' or command == 'back':
			return
		if command == 'yes':
				self.logout()
				print self.addr, "User %s is exiting" % self.userid
				self.discontinue = True
				self.send(exit_message,'main/bye-bye')

		return

	def run(self):
		'''Flow will return here once the thread starts. Ask for login or register (input command)/
		Then login/register function called. Have them both interface with the Datastore class.'''
		first_attempt = True
		while not self.discontinue :
			if not self.logged_in:
				command = self.get_instruction(first_attempt)
				if command == 'login' :
					self.login()
				if command == 'register' :
					self.register()
					self.login()
				if command == 'exit':
					return self.exit()
				first_attempt = False
				continue
			#These commands will be executed only after the user has logged in
			if self.need_help:
				self.help()
				self.need_help = False
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
			if command == 'help':
				self.help()
			if command == 'pings':
				self.pings()
			if command == 'ping':
				self.ping()
			if command == self.userid:
				self.view(view_self = True)
			if command == 'view':
				self.view()
			if command == 'settings':
				self.settings()
			if command == 'logout':
				self.logout()
			if command == 'exit':
				self.exit()

		'''This part of the code will be accessed only while closing the connection'''
		self.client.close
