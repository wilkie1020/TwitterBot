from TwitterAPI import TwitterAPI
import random
import time

#authentication data
consumer_key = "<Your token here>"
consumer_secret = "<Your token here>"
access_token_key = "<Your token here>"
access_token_secret = "<Your token here>"

#Authenticate
api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

#words available
s_nouns = ["Kyle", "John", "Andrew", "Travis", "Ian", "Batman", "Zues", "A bunndy", "A dude", "My mom", "The king", "Some guy", "A cat with rabies", "A sloth", "Your homie", "This cool guy my gardener met yesterday", "Superman"]
p_nouns = ["Very many people", "The knights who say ne", "These dudes", "Both of my moms", "All the kings of the world", "Some guys", "All of a cattery's cats", "The multitude of sloths living under your bed", "Your homies", "Like, these, like, all these people", "Supermen"]
s_verbs = ["eats", "kicks", "gives", "treats", "meets with", "creates", "hacks", "configures", "spies on", "retards", "meows on", "flees from", "tries to automate", "explodes"]
p_verbs = ["ran", "punched", "eat", "kick", "give", "treat", "meet with", "create", "hack", "configure", "spy on", "retard", "meow on", "flee from", "try to automate", "explode"]
infinitives = ["to make a pie.", "for no apparent reason.", "because the sky is green.", "for a disease.", "to be able to make toast explode.", "to know more about archeology."]

def sing_sen_maker():
#Makes a random senctence from the different parts of speech. Uses a SINGULAR subject
	
	string = (random.choice(s_nouns) + " " + random.choice(s_verbs) + " " + random.choice(s_nouns).lower() or random.choice(p_nouns).lower() + " " + random.choice(infinitives))

	print (string + "\n")
	r = api.request('statuses/update', {'status': string})

while(True):
	sing_sen_maker()
	#tweet random sentence every 2 minutes
	time.sleep(120)
