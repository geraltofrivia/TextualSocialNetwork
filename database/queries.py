########################################CREATE TABLE QUERIES########################################


create_users = '''
								CREATE TABLE USERS (
									USERID TEXT PRIMARY KEY NOT NULL,
								 	NAME TEXT NOT NULL,
								 	SEX TEXT NOT NULL 
								 );'''

create_posts = '''
								CREATE TABLE POSTS (
									DATE TEXT NOT NULL,
									TIME TEXT NOT NULL,
									USERID TEXT NOT NULL,
									POSTID TEXT NOT NULL
									);'''

create_subscriptions = '''
								CREATE TABLE SUBSCRIPTIONS (
									USERID TEXT NOT NULL,
									SUBSID TEXT NOT NULL
									);'''

create_pokes = '''
								CREATE TABLE POKES (
									FROMID TEXT NOT NULL,
									TOID TEXT NOT NULL
									);'''

create_ups = '''
								CREATE TABLE UPS (
									POSTID TEXT NOT NULL,
									USERID TEXT NOT NULL
									);'''

########################################INSERT QUERIES########################################

insert_user = '''INSERT INTO USERS
									(USERID, NAME, SEX) \
									VALUES (:userid, :name, :sex) '''

insert_post = '''INSERT INTO POSTS
									(DATE, TIME, USERID, POSTID) \
									VALUES (:date,:time,:userid,:postid) '''

insert_subscription = '''INSERT INTO SUBSCRIPTIONS
													(USERID, SUBSID) \
													VALUES (:userid,:subsid) '''

insert_poke = '''INSERT INTO POKES
									(FROMID, TOID) \
									VALUES (:fromid, :toid) '''

insert_ups = '''INSERT INTO UPS
									(POSTID, USERID) \
									VALUES (:postid,:userid) '''



#Function to fetch create table queries
def getCreateTable():
	return [create_users,create_ups,create_pokes,create_subscriptions,create_posts]

#Functions to fetch insert element queries
def getInsertUser():
	return insert_user 

def getInsertPost():
	return insert_post

def getInsertSubscription():
	return insert_subscription

def getInsertPoke():
	return insert_poke

def getInsertUps():
	return insert_ups	




