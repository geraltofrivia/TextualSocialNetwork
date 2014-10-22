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

	def insert_new_post(self,userid,postid,text):
		query = queries.getInsertPost()
		userid = self.checkText(userid)
		postid = self.checkText(postid)
		text = self.checkText(text)
		if not ( userid == -1 or postid == -1 or text == -1 ):
			timestamp = self.getNow()
			self.cursor.execute(query, {'timestamp':timestamp,'userid':userid,'postid':postid,'data':data} )
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
			self.cursor.execute(query, {'fromid':fromid, 'toid':toid} )
			self.db.commit()
		else:
			print "(Database):Improper Datatype, value rejected"
			#WHAT TO DO NOW?

	def insert_new_up(self,postid,userid):
		query = queries.getInsertUps()
		postid = self.checkText(postid)
		userid = self.checkText(userid)
		if not ( postid == -1 or userid == -1 ):
			self.cursor.execute(query, {'postid':postid,'userid':userid} )
			self.db.commit()
		else:
			print "(Database):Improper Datatype, value rejected"
			#WHAT TO DO NOW?			

	def exit():
		self.db.close()
