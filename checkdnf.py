from TwitterAPI import TwitterAPI
import os.path
import json


#authentication data
consumer_key = "5s1rr9Dg0eKFD97T7w2G6kpe9"
consumer_secret = "DvoVKE1wn2vsWLj8qaZyUnNo5K77KUf2dlO9g6Vzjc1sF7pjE9"
access_token_key = "890686903506173952-912Z2iCvNXo7QEuNjf6aZMW07Ne47bj"
access_token_secret = "2aDT2mjtFO92I59vvD2WBjFWMSnX11q9eyC2l3vTT9k6D"

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
	r = api.request('friendships/destroy', {'user_id': x})
	jason = r.json()
	screen_name = jason['screen_name']
	print(screen_name)