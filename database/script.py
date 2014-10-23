import db
import os

if os.path.isfile("data.db"):			
	os.remove('data.db')

database = db.Datastore()

database.insert_new_user('geralt','priyansh','m')
database.insert_new_user('ian','hor','m')
database.insert_new_user('mom','vinita','f')
database.insert_new_user('dad','ajay','m')

database.insert_new_post('geralt','100','Hey you')
database.insert_new_post('geralt','101','Out there on your own')
database.insert_new_post('geralt','102','Standing naked by the phone')
database.insert_new_post('geralt','103','Can you touch me?')
database.insert_new_post('ian','110','Hey Jude')
database.insert_new_post('ian','111','Dont make it bad')
database.insert_new_post('ian','112','Take a sad song')
database.insert_new_post('ian','113','And make it better')
database.insert_new_post('mom','210','Ive heard there was a secret chord')
database.insert_new_post('mom','211',' That David played, and it pleased the Lord')
database.insert_new_post('mom','212',' But you dont really care for music, do you?')

database.insert_new_up('100','geralt')
database.insert_new_up('100','dad')
database.insert_new_up('101','dad')
database.insert_new_up('102','dad')
database.insert_new_up('110','dad')
database.insert_new_up('110','mom')
database.insert_new_up('110','ian')
database.insert_new_up('110','geralt')

database.insert_new_subscription('geralt','dad')
database.insert_new_subscription('geralt','ian')
database.insert_new_subscription('geralt','mom')
database.insert_new_subscription('dad','mom')
database.insert_new_subscription('dad','ian')
database.insert_new_subscription('ian','geralt')

database.insert_new_poke('geralt','ian')
database.insert_new_poke('dad','mom')
database.insert_new_poke('geralt','dad')

print "USERS"
users = database.get_all_users()
for user in users:
	print user
print "POSTS"
posts = database.get_all_posts(True)
for post in posts:
	print post
print "UPS FOR 110"
ups =  database.get_ups_for('110')
for user in ups:
	print user
print "UPS FOR 100"
ups = database.get_ups_for('100')
for user in ups:
	print user
print "POSTS OF GERALT"
posts = database.get_posts_of('geralt',True)
for post in posts:
	print post
print "SUBSCRIPTIONS OF GERALT"
subs = database.get_subscriptions_of('geralt')
for sub in subs:
	print sub
print "SUBSCRIPTIONS OF MOM"
subs = database.get_subscriptions_of('mom')
for sub in subs:
	print sub
print "POKES TO MOM"
pokes = database.get_pokes_for('mom')
for poke in pokes:
	print poke
print "POSTS FOR GERALT"
posts = database.get_posts_for('geralt')
for post in posts:
	print post
print "TESTING REFERENCE CHECK"
print database.is_existing_userid('geralto')
print database.is_existing_userid('geralt')

database.exit()