#We'll just use this to test the insert that has been implemented?
import db

database = db.Datastore();

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
	database.insert_new_user(id,name,sex)
	print "Success"