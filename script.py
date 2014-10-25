from database.db import Datastore
import os

if os.path.isfile("database/data.db"):			
	os.remove('database/data.db')

database = Datastore()

database.insert_new_user('geralt','priyansh','m','pass')
database.insert_new_user('aura','tanya','f','pass')
database.insert_new_user('ian','hor','m','root')
database.insert_new_user('mom','vinita','f','mod')
database.insert_new_user('dad','ajay','m','admin')

database.insert_new_post('geralt','Hey you')
database.insert_new_post('geralt','Out there on your own')
database.insert_new_post('geralt','Standing naked by the phone')
database.insert_new_post('geralt','Can you touch me?')
database.insert_new_post('ian','Hey Jude')
database.insert_new_post('ian','Dont make it bad')
database.insert_new_post('ian','Take a sad song')
database.insert_new_post('ian','And make it better')
database.insert_new_post('mom','Ive heard there was a secret chord')
database.insert_new_post('mom',' That David played, and it pleased the Lord')
database.insert_new_post('mom',' But you dont really care for music, do you?')
database.insert_new_post('aura','Theres a lady whos sure')
database.insert_new_post('aura','All that glitters is gold')
database.insert_new_post('aura','And shes buying a stairway to heaven')

database.insert_new_up('10','geralt')
database.insert_new_up('10','dad')
database.insert_new_up('1','dad')
database.insert_new_up('2','dad')
database.insert_new_up('5','dad')
database.insert_new_up('5','mom')
database.insert_new_up('5','ian')
database.insert_new_up('5','geralt')
database.insert_new_up('3','geralt')

database.insert_new_subscription('geralt','dad')
database.insert_new_subscription('geralt','ian')
database.insert_new_subscription('geralt','mom')
database.insert_new_subscription('dad','mom')
database.insert_new_subscription('dad','ian')
database.insert_new_subscription('ian','geralt')

database.insert_new_ping('geralt','ian')
database.insert_new_ping('dad','mom')
database.insert_new_ping('geralt','dad')
database.insert_new_ping('dad','ian')
database.insert_new_ping('dad','ian')
database.insert_new_ping('dad','ian')
database.insert_new_ping('dad','ian')
database.insert_new_ping('dad','ian')
database.insert_new_ping('dad','ian')
database.insert_new_ping('dad','ian')
database.insert_new_ping('dad','ian')
database.insert_new_ping('dad','ian')
database.insert_new_ping('dad','ian')
database.insert_new_ping('dad','ian')
database.insert_new_ping('dad','ian')
database.insert_new_ping('dad','ian')
database.insert_new_ping('mom','ian')
database.insert_new_ping('mom','ian')
database.insert_new_ping('mom','ian')
database.insert_new_ping('mom','ian')
database.insert_new_ping('mom','ian')
database.insert_new_ping('mom','ian')
database.insert_new_ping('dad','ian')
database.insert_new_ping('dad','ian')
database.insert_new_ping('mom','ian')
database.insert_new_ping('mom','ian')
database.insert_new_ping('mom','ian')
database.insert_new_ping('mom','ian')
database.insert_new_ping('mom','ian')
database.insert_new_ping('dad','ian')
database.insert_new_ping('dad','ian')
database.insert_new_ping('dad','ian')
database.insert_new_ping('mom','ian')
database.insert_new_ping('mom','ian')
database.insert_new_ping('mom','ian')
database.insert_new_ping('dad','ian')
database.insert_new_ping('dad','ian')

print "USERS"
users = database.get_all_users()
for user in users:
	print user
print "POSTS"
posts = database.get_all_posts(True)
for post in posts:
	print post
print "UPS FOR 5"
ups =  database.get_ups_for('5')
for user in ups:
	print user
print "UPS FOR 1"
ups = database.get_ups_for('1')
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
print "PINGS TO MOM"
pings = database.get_pings_for('mom')
for ping in pings:
	print ping
print "POSTS FOR GERALT"
posts = database.get_posts_for('geralt')
for post in posts:
	print post
print "TESTING REFERENCE CHECK"
print database.is_existing_userid('geralto')
print database.is_existing_userid('geralt')
print "CHECK PASSWORD"
print database.check_credentials('geralt','pass')
print database.check_credentials('geralt','pas')
print "CHECK GET UPS OF GERALT"
ups = database.get_ups_of('geralt',True)
print ups
database.exit()