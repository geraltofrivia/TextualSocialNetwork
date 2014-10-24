
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

	def is_existing_userid(self,userid):
		'''Returns var or -1 verifying if the userid exists in the database'''
		query = queries.getFindUser()
		self.cursor.execute(query, {'userid':userid} )
		result = []
		for user in self.cursor:
			result.append(user)
		if len(result) > 0:
			return userid
		else:
			return -1

	def is_existing_postid(self,postid):
		'''Returns var or -1, verifying if the postid exists in the database'''
		query = queries.getFindPost()
		self.cursor.execute(query, {'postid':postid} )
		result = []
		for post in self.cursor:
			result.append(post)
		if len(result) > 0:
			return postid
		else:
			return -1

	def insert_new_user(self,userid,name,sex,password):
		query = queries.getInsertUser()
		userid = self.checkText(userid)
		name = self.checkText(name)
		sex = self.checkSex(sex)
		password = self.checkText(password)

		if userid == -1:
			print "(Database: Insert User):Improper Datatype, value rejected. userid:",userid,'\tname:',name,'\tsex:',sex
			return -1
		if name == -1:
			print "(Database: Insert User):Improper Datatype, value rejected. userid:",userid,'\tname:',name,'\tsex:',sex
			return -2
		if sex == -1:
			print "(Database: Insert User):Improper Datatype, value rejected. userid:",userid,'\tname:',name,'\tsex:',sex
			return -3
		if password == -1:
			print "(Database: Insert User):Improper Datatype, value rejected. userid:",userid,'\tname:',name,'\tsex:',sex
			return -4
		self.cursor.execute( query, {'userid':userid,'name':name,'sex':sex,'password':password} )
		self.db.commit()
		return 0

	def insert_new_post(self,userid,postid,content):
		query = queries.getInsertPost()
		userid = self.is_existing_userid(userid)
		postid = self.checkText(postid)		
		if userid == -1:
			print "(Database: Insert Post):Improper Datatype, value rejected. userid:",userid,'\tpostid:',postid,'\tcontent:',content
			return -1
		if postid == -1:
			print "(Database: Insert Post):Improper Datatype, value rejected. userid:",userid,'\tpostid:',postid,'\tcontent:',content
			return -2
		timestamp = self.getNow()
		self.cursor.execute(query, {'timestamp':timestamp,'userid':userid,'postid':postid,'content':content} )
		self.db.commit()
		return 0

	def insert_new_subscription(self,userid,subsid):
		query = queries.getInsertSubscription()
		userid = self.is_existing_userid(userid)
		subsid = self.is_existing_userid(subsid)
		if userid == -1:
			print "(Database: Insert Subscription):Improper Datatype, value rejected. userid:",userid,'\tsubsid:',subsid
			return -1
		if subsid == -1:
			print "(Database: Insert Subscription):Improper Datatype, value rejected. userid:",userid,'\tsubsid:',subsid
			return -2
		self.cursor.execute(query, {'userid':userid,'subsid':subsid} )
		self.db.commit()
		return 0

	def insert_new_poke(self,fromid,toid):
		query = queries.getInsertPoke()
		fromid = self.is_existing_userid(fromid)
		toid = self.is_existing_userid(toid)
		if toid == -1:
			print "(Database: Insert Poke):Improper Datatype, value rejected. fromid:",fromid,'\ttoid:',toid
			return -1
		if fromid == -1:
			print "(Database: Insert Poke):Improper Datatype, value rejected. fromid:",fromid,'\ttoid:',toid
			return -2
		self.cursor.execute(query, {'fromid':fromid,'toid':toid} )
		self.db.commit()
		return 0

	def insert_new_up(self,postid,userid):
		query = queries.getInsertUp()
		postid = self.is_existing_postid(postid)
		userid = self.is_existing_userid(userid)
		if postid == -1:
			print "(Database: Insert Up):Improper Datatype, value rejected. postid:",postid,'\tuserid:',userid
			return -1
		if userid == -1:
			print "(Database: Insert Up):Improper Datatype, value rejected. postid:",postid,'\tuserid:',userid
			return -2
		self.cursor.execute(query, {'postid':postid,'userid':userid} )
		self.db.commit()
		return 0
		
	def get_all_users(self):
		'''Return a list of tuple (userid,name,sex) for all users'''
		query = queries.getAllUsers()
		self.cursor.execute(query)
		result = []
		for user in self.cursor:
			result.append(user)			
		return result

	def get_all_posts(self,get_ups=False):
		'''Returns a list of tuple (postid,text,userid,timestamp) for all posts. 
		If parameter is true, returns number of ups per post as well'''	
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

	def get_posts_of(self,userid,get_ups=False):
		'''Returns a list of tuple (postid,text,userid,timestamp) for posts of a specific user 
		If parameter is true, returns number of ups per post as well'''
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

	def get_posts_for(self,userid,get_ups=False):
		'''Returns a list of tuple (postid, text, userid, timestamp)
		collected from the users which are subscribed by this user. This can directly be fed in a timeline
		If parameter is true, returns number of ups per post as well'''
		subs = self.get_subscriptions_of(userid)
		result = []
		for user in subs:
			posts = self.get_posts_of(user,get_ups)
			result = result + posts
		return sorted(result, key=lambda x : x[3], reverse = True)

	def get_subscriptions_of(self,userid):
		'''Return a list of userid whose posts are to be fetched for this user
		In other words, returns a list of subscriptions for this user'''
		query = queries.getSubscriptionsOfUser()
		self.cursor.execute(query, {'userid':userid} )
		result = []
		for subscription in self.cursor:
			result.append(subscription[1])
		return result

	def get_pokes_by(self,userid):
		'''Returns a list of userids of people whom this user has poked'''
		query = queries.getPokesByUser()
		self.cursor.execute(query, {'userid':userid} )
		result = []
		for user in self.cursor:
			result.append(user[0])
		return result		

	def get_pokes_for(self,userid):
		'''Returns a list of userids who have poked this user'''
		query = queries.getPokesToUser()
		self.cursor.execute(query, {'userid':userid} )
		result = []
		for user in self.cursor:
			result.append(user[0])
		return result		
	
	def get_all_pokes(self):
		'''Returns a list of tuple (from, to) of pokes in the database'''
		query = queries.getPokes()
		self.cursor.execute(query)
		result = []
		for poke in self.cursor:
			result.append(poke)
		return result

	def get_ups_for(self,postid):
		'''Returns a list of userids who have upped a post'''
		query = queries.getUpsToPost()
		self.cursor.execute(query, {'postid':postid} )
		result = []
		for ups in self.cursor:
			result.append(ups[0])
		return result


	def check_credentials(self,userid,password):
		'''Returns True/False if the userid and password match'''
		query = queries.getFindUser()
		self.cursor.execute(query, {'userid':userid} )
		result = []
		for user in self.cursor:
			result.append(user)
		if len(result) <= 0:
			return False	
		return result[0][3] == password

	def exit(self):
		self.db.close()
