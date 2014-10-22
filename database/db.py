import sqlite3
import os
import queries


Class Datastore:
	def __init__():
	flag_init = False		
	if not os.path.isfile("data.db"):
		#The DB doesn't yet exist. 
		#This flag implies that we ought to create tables
		flag_init = True

	db = sqlite3.connect('data.db')
	cursor = db.cursor()
	print "(Database):Database Connected"

	#If the database doesn't exist already 
	if flag_init:
		for table in queries.getCreateTable():
			cursor.execute(table)
			print "(Database):Table created successfully"

