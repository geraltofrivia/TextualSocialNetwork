########################################CREATE TABLE QUERIES########################################

create_users = '''
								CREATE TABLE USERS (
									USERID TEXT PRIMARY KEY NOT NULL,
								 	NAME TEXT NOT NULL,
								 	SEX TEXT NOT NULL 
								 );'''

create_posts = '''
								CREATE TABLE POSTS (
									TIMESTAMP TEXT NOT NULL,
									USERID TEXT NOT NULL,
									POSTID TEXT PRIMARY KEY NOT NULL,
									CONTENT TEXT NOT NULL
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
									(TIMESTAMP, USERID, POSTID, CONTENT) \
									VALUES (:timestamp,:userid,:postid,:content) '''

insert_subscription = '''INSERT INTO SUBSCRIPTIONS
													(USERID, SUBSID) \
													VALUES (:userid,:subsid) '''

insert_poke = '''INSERT INTO POKES
									(FROMID, TOID) \
									VALUES (:fromid,:toid) '''

insert_up = '''INSERT INTO UPS
									(POSTID, USERID) \
									VALUES (:postid,:userid) '''

########################################QUERIES########################################

all_users = '''SELECT USERID, NAME, SEX 
								FROM USERS'''

all_posts = '''SELECT POSTID, CONTENT, USERID, TIMESTAMP
								FROM POSTS
								ORDER BY TIMESTAMP DESC'''

all_posts_by_user = '''SELECT POSTID, CONTENT, USERID, TIMESTAMP
												FROM POSTS
												WHERE USERID = :userid
												ORDER BY TIMESTAMP DESC'''

all_subscriptions_of_user = '''SELECT USERID, SUBSID
																FROM SUBSCRIPTIONS
																WHERE USERID = :userid'''

all_pokes_by_user = '''SELECT TOID
												FROM POKES
												WHERE FROMID = :userid'''

all_pokes_to_user = '''SELECT FROMID
												FROM POKES
												WHERE TOID = :userid'''

all_pokes = '''SELECT FROMID, TOID
								FROM POKES'''
																
all_ups_to_post = '''SELECT USERID
											FROM UPS
											WHERE POSTID = :postid'''				

find_user = '''SELECT USERID, NAME, SEX
								FROM USERS
								WHERE USERID = :userid'''

find_post = '''SELECT POSTID, CONTENT, USERID, TIMESTAMP
								FROM POSTS
								WHERE POSTID = :postid'''

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

def getInsertUp():
	return insert_up

#Functions to fetch query request queries :/ 
def getAllUsers():
	return all_users

def getAllPosts():
	return all_posts

def getPostsByUser():
	return all_posts_by_user

def getSubscriptionsOfUser():
	return all_subscriptions_of_user

def getPokesByUser():
	return all_pokes_by_user

def getPokesToUser():
	return all_pokes_to_user

def getPokes():
	return all_pokes

def getUpsToPost():
	return all_ups_to_post

def getFindUser():
	return find_user

def getFindPost():
	return find_post
