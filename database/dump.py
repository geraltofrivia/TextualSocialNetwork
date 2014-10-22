import sqlite3
import os

flag_init = False		#Flag depicting if the db is being created for the first time
#SQL STATEMENTS
create_table = '''
								CREATE TABLE REGISTRY (
									ID TEXT PRIMARY KEY NOT NULL,
								 	NAME TEXT NOT NULL,
								 	SEX TEXT NOT NULL
								 );'''

insert = ''' INSERT INTO REGISTRY (ID, NAME, SEX) \
							VALUES (:id, :name, :sex) '''



if not os.path.isfile("users.db"):
	#The DB doesn't yet exist. Implies that we ought to create tables
	flag_init = True

db = sqlite3.connect('users.db')
cursor = db.cursor()
print "opened database successfully"

if flag_init:
	cursor.execute(create_table)
	print "Table created successfully"

while True:
	command = raw_input()
	if command == 'insert':
		print "Enter desired ID"
		id = raw_input()
		print "Enter desired name"
		name = raw_input()
		print "Enter m/f"
		sex = raw_input()
		if sex == 'm':
			sex = 'male'
		elif sex == 'f':
			sex == 'female'
		cursor.execute(insert, {'name':name, 'id':id, 'sex':sex})
		confirm = cursor.lastrowid
		print 'REGISTRATION COMPLETE. Please use this id to refer to yourself henceforth - ', confirm
		db.commit()
	if command == 'quit':
		db.close()
		break



