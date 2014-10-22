import sqlite3
import os
import queries

class Datastore:
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
		self.cursor.execute(query, {'userid':userid,'name':name,'sex':sex} )
		self.db.commit()

	def exit():
		self.db.close()
