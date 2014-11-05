
import sqlite3
import os
import queries
import datetime

class Helper:
	def checkText(self,var):
		if var.isalnum() and len(var) > 1:
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

	def checkBoolean(self,var):
		if var.lower()[0] == 't':
			return 'True'
		if var.lower()[0] == 'f':
			return 'False'
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
		if not os.path.isfile("database/data.db"):			
			flag_init = True

		self.db = sqlite3.connect('database/data.db', check_same_thread=False)
		self.cursor = self.db.cursor()
		print "(Database):Database Connected"
		if flag_init:
			#Initialize the Database Tables
			for table in queries.getCreateTable():
				self.cursor.execute(table)
				print "(Database):Table created successfully"

	def is_existing_userid(self,userid,reverse = False):
		'''Returns var or -1 verifying if the userid exists in the database
		If reverse - True: return var if user doesnt exist & return -1 if user exists
		If reverse - False: return -1 if user doesnt exist & return var if user exists'''
		query = queries.getFindUser()
		self.cursor.execute(query, {'userid':userid} )
		result = []
		for user in self.cursor:
			result.append(user)
		bool_result = len(result) > 0
		if bool_result != reverse:
			#Logical XOR between two boolean values, for our purpose
			return userid
		else:
			return -1

	def is_existing_postid(self,postid,reverse = False):
		'''Returns var or -1 verifying if the userid exists in the database
		If reverse - True: return var if user doesnt exist & return -1 if user exists
		If reverse - False: return -1 if user doesnt exist & return var if user exists'''
		query = queries.getFindPost()
		self.cursor.execute(query, {'postid':postid} )
		result = []
		for post in self.cursor:
			result.append(post)
		bool_result = len(result) > 0 
		if bool_result != reverse:
			return postid
		else:
			return -1

	def is_not_empty(self,var):
		if len(str(var)) < 1:
			return -1
		return var

	def insert_new_user(self,userid,name,sex,password,visible = 'true'):
		query = queries.getInsertUser()
		userid = self.is_existing_userid(userid, reverse = True)
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
		self.cursor.execute( query, {'userid':userid,'name':name,'sex':sex,'password':password,'visible':visible} )
		self.db.commit()
		return 0

	def insert_new_post(self,userid,content,find_mentions = True):
		query = queries.getInsertPost()
		userid = self.is_existing_userid(userid)
		content = self.is_not_empty(content)
		if content == -1:
			print "(Database: Insert Post):Improper Datatype, value rejected. userid:",userid,'\tcontent:',content
			return -1
		if userid == -1:
			print "(Database: Insert Post):Improper Datatype, value rejected. userid:",userid,'\tcontent:',content
			return -2
		timestamp = self.getNow()
		self.cursor.execute(query, {'timestamp':timestamp,'userid':userid,'content':content} )
		self.db.commit()
		if find_mentions:
			self.find_users_in_post( self.get_post_data( self.cursor.lastrowid ) )
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

	def insert_new_ping(self,fromid,toid):
		query = queries.getInsertPing()
		fromid = self.is_existing_userid(fromid)
		toid = self.is_existing_userid(toid)
		if toid == -1:
			print "(Database: Insert Ping):Improper Datatype, value rejected. fromid:",fromid,'\ttoid:',toid
			return -1
		if fromid == -1:
			print "(Database: Insert Ping):Improper Datatype, value rejected. fromid:",fromid,'\ttoid:',toid
			return -2
		timestamp = self.getNow()
		self.cursor.execute(query, {'fromid':fromid,'toid':toid,'timestamp':timestamp} )
		self.db.commit()
		return 0

	def insert_new_mention(self,userid,postid):
		query = queries.getInsertMention()
		userid = self.is_existing_userid(userid)
		postid = self.is_existing_postid(postid)
		if userid == -1:
			print "(Database: Insert Mention):Improper Datatype, value rejected. userid:",userid,'\tpostid:',postid
			return -1
		if postid == -1:
			print "(Database: Insert Mention):Improper Datatype, value rejected. userid:",userid,'\tpostid:',postid
			return -2
		self.cursor.execute(query, {'userid':userid,'postid':postid} )
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
		timestamp = self.getNow()
		self.cursor.execute(query, {'postid':postid,'userid':userid,'timestamp':timestamp} )
		self.db.commit()
		return 0
		
	def get_all_users(self):
		'''Return a list of tuple (userid,name,sex) for all users'''
		query = queries.getAllUsers()
		self.cursor.execute(query)
		result = []
		for user in self.cursor:
			if not user[-1].lower() == 'true':
				continue			
			result.append(user)
		return result

	def get_user_data(self,userid):
		'''Returns one tuple containing the entry in users table for this user'''
		query = queries.getFindUser()
		self.cursor.execute(query, {'userid':userid} )
		result = []
		for user in self.cursor:
			result.append(user)
		if len(result) < 1:
			return 0
		return result[0]

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

	def get_post_data(self,postid,get_ups = False):
		'''Returns one tuple containing the entry in posts table for this post'''
		query = queries.getFindPost()
		self.cursor.execute(query, {'postid':postid} )
		result = []
		for user in self.cursor:
			for element in user:
				result.append(element)
		if get_ups:
			ups = self.get_ups_for(result[0])
			result.append(len(ups))
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
		If parameter is true, returns number of ups per post as well

		v0.7 onwards - fetches post which have mention for the given user id.'''
		subs = self.get_subscriptions_of(userid)
		result = []
		for user in subs:
			posts = self.get_posts_of(user,get_ups)
			result = result + posts
		#Fetch mentions too
		mentions = self.get_mentions_of(userid)
		for mention in mentions:
			post_data = self.get_post_data(mention,get_ups)
			if not post_data in result:
				result.append(post_data)
		return sorted(result, key=lambda x : x[3], reverse = True)

	def get_subscriptions_of(self,userid):
		'''Return a list of userid whose posts are to be fetched for this user
		In other words, returns a list of subscriptions for this user (Whom he has subscribed to)'''
		query = queries.getSubscriptionsOfUser()
		self.cursor.execute(query, {'userid':userid} )
		result = []
		for subscription in self.cursor:
			result.append(subscription[1])
		return result

	def get_subscribers_of(self,subsid):
		'''Return a list of users who have subscribed to this user'''
		query = queries.getSubscribersOfUser()
		self.cursor.execute(query, {'subsid':subsid} )
		result = []
		for subscription in self.cursor:
			result.append(subscription)
		return result

	def get_all_mentions(self):
		'''Returns a python list of all the mentions stored in the database'''
		query = queries.getAllMentions()
		self.cursor.execute(query)
		result = []
		for mention in self.cursor:
			result.append(mention)
		return result

	def get_mentions_of(self,userid):
		'''Returns postid for all the posts which mention the given user somewhere'''
		query = queries.getMentionsOfUser()
		self.cursor.execute(query, {'userid':userid} )
		result = []
		for mention in self.cursor:
			result.append(mention[1])
		return result

	def get_pings_by(self,userid):
		'''Returns a list of userids of people whom this user has pinged'''
		query = queries.getPingsByUser()
		self.cursor.execute(query, {'userid':userid} )
		result = []
		for user in self.cursor:
			result.append(user[0])
		return result		

	def get_pings_for(self,userid):
		'''Returns a list of userids who have pinged this user'''
		query = queries.getPingsToUser()
		self.cursor.execute(query, {'userid':userid} )
		result = []
		for user in self.cursor:
			result.append(user[0])
		return result		
	
	def get_all_pings(self):
		'''Returns a list of tuple (from, to) of pings in the database'''
		query = queries.getPings()
		self.cursor.execute(query)
		result = []
		for ping in self.cursor:
			result.append(ping)
		return result

	def get_ups_for(self,postid):
		'''Returns a list of userids who have upped a post'''
		query = queries.getUpsToPost()
		self.cursor.execute(query, {'postid':postid} )
		result = []
		for ups in self.cursor:
			result.append(ups[0])
		return result

	def get_ups_of(self,userid,get_ups = True):
		'''Returns a list of posts who have been upped by this user'''
		query =queries.getUpsOfUser()
		self.cursor.execute(query, {'userid':userid} )
		result = []
		for post in self.cursor:
			result.append(post)
		final = []
		for up in result:
			data =  self.get_post_data(up[1],get_ups)
			final.append(data)
		return final

	def update_user_visible(self,userid,visible):
		'''Update the user setting for being visible or not'''
		query = queries.getUpdateUser()
		userid = self.is_existing_userid(userid)
		visible = self.checkBoolean(visible)

		if userid == -1:
			return -1
		if visible == -1:
			return -2
		self.cursor.execute(query, {'userid':userid, 'visible':visible} )
		self.db.commit()
		return 0

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

	def find_users_in_post(self,post):
		'''This function returns a list of all the users that are in a post. Returns an empty list otherwise
		It looks for an '@' in the string, When found, it will detect usernames like @geralt but not geralt or @ geralt.'''
		users =  self.get_all_users()
		index = 0
		users_found = []
		content = post[1]
		postid = post[0]
		while True:
			index = content.find('@',index)
			if index == -1:
				break
			word = content[index:].split()[0]
			for user in users:
				if word.startswith('@'+user[0]):
					users_found.append(user[0])
					self.insert_new_mention(user[0],postid)
			index += 2
		return users_found

	def exit(self):
		self.db.close()
