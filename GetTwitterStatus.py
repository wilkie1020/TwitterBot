from TwitterAPI import TwitterAPI
import json


#authentication data
consumer_key = "<Your token here>"
consumer_secret = "<Your token here>"
access_token_key = "<Your token here>"
access_token_secret = "<Your token here>"

#Authenticate
api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

r = api.request('account/verify_credentials').json()

for x in r:
	print(x + "\n")

#r = api.request('users/lookup', {'user_id': id})
r = api.request('application/rate_limit_status').json()

for x in r:
	print(x + "\n")