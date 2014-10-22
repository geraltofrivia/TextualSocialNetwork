create_users = '''
								CREATE TABLE USERS (
									USERID TEXT PRIMARY KEY NOT NULL,
								 	NAME TEXT NOT NULL,
								 	SEX TEXT NOT NULL 
								 );'''

create_post = '''
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

create_poke = '''
								CREATE TABLE POKE (
									FROMID TEXT NOT NULL,
									TOID TEXT NOT NULL
									);'''

create_ups = '''
								CREATE TABLE UPS (
									POSTID TEXT NOT NULL,
									USERID TEXT NOT NULL
									);'''

#Function to fetch create table queries
def getCreateTable():
	return [create_users,create_ups,create_poke,create_subscriptions,create_post]




