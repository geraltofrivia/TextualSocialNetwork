#We'll just use this to test the insert that has been implemented?
import db

database = db.Datastore();

id = 'ger'
name = 'pri'
sex = 'm'
database.insert_new_user(id,name,sex)
print "Success"