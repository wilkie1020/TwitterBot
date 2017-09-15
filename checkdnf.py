from TwitterAPI import TwitterAPI
import os.path
import json


#authentication data
consumer_key = "<YOUR KEY HERE>"
consumer_secret = "<YOUR KEY HERE>"
access_token_key = "<YOUR KEY HERE>"
access_token_secret = "<YOUR KEY HERE>"

#Authenticate
api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)


donotfollow = list()# bots and such - never follow or retweet

if os.path.isfile('C:\\Users\\Mat\\AppData\\Local\\Programs\\Python\\Python36-32\\Working Folder\\ContestBot\\donotfollow'):
	print("Loading do not follow list \n")
	with open('C:\\Users\\Mat\\AppData\\Local\\Programs\\Python\\Python36-32\\Working Folder\\ContestBot\\donotfollow') as h:
		donotfollow = h.read().splitlines()
	h.close()
	
	
for x in donotfollow:
	r = api.request('users/show', {'id': x})
	jason = r.json()
	screen_name = jason['screen_name']
	print(screen_name)