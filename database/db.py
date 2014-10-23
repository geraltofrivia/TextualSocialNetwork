
import sqlite3
import os
import queries
import datetime

class Helper:
	def checkText(self,var):
		if var.isalnum():
			return var
		else:
			return -1

	def checkInt(self,var):
		if var.isdigit():
			return var
		else:
			return -1
	
	def checkDateTime(self,var):
		try:
			var = datetime.datetime.strptime(var, '%Y-%m-%d %H:%M:%S')
			return var
		except ValueError:
			raise ValueError("Incorrect data format, should be YYYY-MM-DD")
			return -1

	def checkSex(self,var):
		if var[0] == 'm':
			return 'male'
		if var[0] == 'f':
			return 'female'
		else:
			return -1

	def getNow(self):
		return str(datetime.datetime.now())

''' The datastore class will interface all the functions that will be required of the database
Once instantiated, it will automatically generate tables and create and connect to database
All the insert queries will return 0 or -1 based on the success of the insert operation
All the search queries will return a list of all the elements found

Open one instance of this class per active user/operating class.
And close the database instance once the user disconnects
To close the database after the operations are done, call the exit() function.
'''
class Datastore(Helper):
	def __init__(self):
		flag_init = False		
		#If the database doesn't yet exist, set flag.
		if not os.path.isfile("data.db"):			
			flag_init = True

		self.db = sqlite3.connect('data.db')
		self.cursor = self.db.cursor()
		print "(Database):Database Connected"
		if flag_init:
			#Initialize the Database Tables
			for table in queries.getCreateTable():
				self.cursor.execute(table)
				print "(Database):Table created successfully"

	def insert_new_user(self,userid,name,sex):
		query = queries.getInsertUser()
		userid = self.checkText(userid)
		name = self.checkText(name)
		sex = self.checkSex(sex)
		if not ( userid == -1 or name == -1 or sex == -1 ):
			self.cursor.execute( query, {'userid':userid,'name':name,'sex':sex} )
			self.db.commit()
		else:
			print "(Database):Improper Datatype, value rejected"
			#WHAT TO DO NOW?

	def insert_new_post(self,userid,postid,content):
		query = queries.getInsertPost()
		userid = self.checkText(userid)
		postid = self.checkText(postid)
		if not ( userid == -1 or postid == -1):
			timestamp = self.getNow()
			self.cursor.execute(query, {'timestamp':timestamp,'userid':userid,'postid':postid,'content':content} )
			self.db.commit()
		else:
			print "(Database):Improper Datatype, value rejected"
			#WHAT TO DO NOW?

	def insert_new_subscription(self,userid,subsid):
		query = queries.getInsertSubscription()
		userid = self.checkText(userid)
		subsid = self.checkText(subsid)
		if not ( userid == -1 or subsid == -1 ):
			self.cursor.execute(query, {'userid':userid,'subsid':subsid} )
			self.db.commit()
		else:
			print "(Database):Improper Datatype, value rejected"
			#WHAT TO DO NOW?

	def insert_new_poke(self,fromid,toid):
		query = queries.getInsertPoke()
		fromid = self.checkText(fromid)
		toid = self.checkText(toid)
		if not ( toid == -1 or fromid == -1 ):
			self.cursor.execute(query, {'fromid':fromid,'toid':toid} )
			self.db.commit()
		else:
			print "(Database):Improper Datatype, value rejected"
			#WHAT TO DO NOW?

	def insert_new_up(self,postid,userid):
		query = queries.getInsertUp()
		postid = self.checkText(postid)
		userid = self.checkText(userid)
		if not ( postid == -1 or userid == -1 ):
			self.cursor.execute(query, {'postid':postid,'userid':userid} )
			self.db.commit()
		else:
			print "(Database):Improper Datatype, value rejected"
			#WHAT TO DO NOW?			

	'''Return a list of tuple (userid,name,sex) for all users'''
	def get_all_users(self):
		query = queries.getAllUsers()
		self.cursor.execute(query)
		result = []
		for user in self.cursor:
			result.append(user)			
		return result

	'''Returns a list of tuple (postid,text,userid,timestamp) for all posts. 
	If parameter is true, returns number of ups per post as well'''
	def get_all_posts(self,get_ups=False):
		query = queries.getAllPosts()
		self.cursor.execute(query)
		result = []
		for post in self.cursor:
			result.append(post)	
		if get_ups:
			final = []
			for post in result:
				ups = self.get_ups_for(post[0])
				set = []
				for element in post:
					set.append(element)
				set.append(len(ups))
				final.append(set)
			return final
		return result

	'''Returns a list of tuple (postid,text,userid,timestamp) for posts of a specific user 
	If parameter is true, returns number of ups per post as well'''
	def get_posts_of(self,userid,get_ups=False):
		query = queries.getPostsByUser()
		self.cursor.execute(query, {'userid':userid} )
		result = []
		for post in self.cursor:
			result.append(post)	
		if get_ups:
			final = []
			for post in result:
				ups = self.get_ups_for(post[0])
				set = []
				for element in post:
					set.append(element)
				set.append(len(ups))
				final.append(set)
			return final
		return result

	'''Returns a list of tuple (postid, text, userid, timestamp)
	collected from the users which are subscribed by this user. This can directly be fed in a timeline
	If parameter is true, returns number of ups per post as well'''
	def get_posts_for(self,userid,get_ups=False):
		subs = self.get_subscriptions_of(userid)
		result = []
		for user in subs:
			posts = self.get_posts_of(user,get_ups)
			result = result + posts
		return result

	'''Return a list of userid whose posts are to be fetched for this user
	In other words, returns a list of subscriptions for this user'''
	def get_subscriptions_of(self,userid):
		query = queries.getSubscriptionsOfUser()
		self.cursor.execute(query, {'userid':userid} )
		result = []
		for subscription in self.cursor:
			result.append(subscription[1])
		return result

	'''Returns a list of userids of people whom this user has poked'''
	def get_pokes_by(self,userid):
		query = queries.getPokesByUser()
		self.cursor.execute(query, {'userid':userid} )
		result = []
		for user in self.cursor:
			result.append(user[0])
		return result		

	'''Returns a list of userids who have poked this user'''
	def get_pokes_for(self,userid):
		query = queries.getPokesToUser()
		self.cursor.execute(query, {'userid':userid} )
		result = []
		for user in self.cursor:
			result.append(user[0])
		return result		
	
	'''Returns a list of tuple (from, to) of pokes in the database'''
	def get_all_pokes(self):
		query = queries.getPokes()
		self.cursor.execute(query)
		result = []
		for poke in self.cursor:
			result.append(poke)
		return result

	'''Returns a list of userids who have upped a post'''
	def get_ups_for(self,postid):
		query = queries.getUpsToPost()
		self.cursor.execute(query, {'postid':postid} )
		result = []
		for ups in self.cursor:
			result.append(ups[0])
		return result

	def exit(self):
		self.db.close()
