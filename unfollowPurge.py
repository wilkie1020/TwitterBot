from TwitterAPI import TwitterAPI
import time

# Authetnication keys
consumer_key = "5s1rr9Dg0eKFD97T7w2G6kpe9"
consumer_secret = "DvoVKE1wn2vsWLj8qaZyUnNo5K77KUf2dlO9g6Vzjc1sF7pjE9"
access_token_key = "890686903506173952-912Z2iCvNXo7QEuNjf6aZMW07Ne47bj"
access_token_secret = "2aDT2mjtFO92I59vvD2WBjFWMSnX11q9eyC2l3vTT9k6D"

# Authenticate
api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

for id in api.request('friends/ids'):
	r = api.request('friendships/destroy', {'user_id': id})
	time.sleep(5)