from TwitterAPI import TwitterAPI
import textwrap
import time
import json
import os.path
import os
import sys
import datetime

#authentication data
consumer_key = "<Your token here>"
consumer_secret = "<Your token here>"
access_token_key = "<Your token here>"
access_token_secret = "<Your token here>"

#Authenticate
api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

#keywords data
follow_key = ["follow", "follower", "must be following", "following"]
fav_key = ["favorite", "fav", "like"]
search_queries = ["emergency", "help", "donate", "RT to win", "retweet to win", "retweet to enter", "rt to enter", "#retweet to #win", "#retweet to win"]
#search_queries = ["RT to win"]
bot_check = ["bot", "b0t"]#May append more like 6 for Bs or 7 for Ts?


#tracking lists
ignorelist = list()# already processed tweets
followlist = list()# who am I following and when
donotfollow = list()# bots and such - never follow or retweet

count_per_Search = 25

tweet_queue = list()#the list of items to re-tweet/favorite/follow

track_file_path = ""


# read in the previous data of tracking lists if they exist
if os.path.isfile(track_file_path + 'ignorelist'):
	print("Loading ignore list \n")
	with open(track_file_path + 'ignorelist') as f:
		ignorelist = f.read().splitlines()
	f.close()
	
if os.path.isfile(track_file_path + 'followlist'):
	print("Loading follow list \n")
	with open(track_file_path + 'followlist') as g:
		followlist = g.read().splitlines()
	g.close()
	
if os.path.isfile(track_file_path + 'donotfollow'):
	print("Loading do not follow list \n")
	with open(track_file_path + 'donotfollow') as h:
		donotfollow = h.read().splitlines()
	h.close()
	
def logNprint(item):
	#item = item.replace("\n","")
	
	print(item)
	
	f_log = open(track_file_path + "log", 'a', encoding='utf-8')
	f_log.write(item)
	f_log.close()

def unFollowBot():
    #This function will see how long a user has been followed
    #for and unfollow if greater than 3 weeks
	today = datetime.datetime.now().date()
    #iterate each item in the follow list
    #O(n), not great, whatever
	for i in range(len(followlist)):
		item = followlist[i]
		
		id, f_date_str = item.split('_')#Splits it based on delimeter _
        #need to see what format datetime is in
		#print(f_date_str)
		f_date_init = datetime.datetime.strptime(f_date_str, "%Y-%m-%d")#need to convert follow date to storing only year month day as well
		#YYYY-MM-DD is the standard form of a datetime.date()
		f_date = f_date_init.date()
		#print(str(f_date))
        
		d_diff = today - f_date
		d_diff_int = int(d_diff.days)
        
		if d_diff_int > 21:
			try:
				r = api.request('friendships/destroy', {'user_id': id})
				followlist.pop(i)
				toprint = "Unfollowed after 3 months: " + id
				logNprint(toprint)
			except:
				logNprint("Error Occured. Unfollow failed \n")
		
	logNprint("Unfollowing all in do not follow list \n")
	for x in donotfollow:
		try:
			r = api.request('users/lookup', {'user_id': x})
			logNprint(r['following'])
			if(r['following'] == True):
				try:
					r = api.request('friendships/destroy', {'user_id': x})
					toprint = "Unfollowed bot from do not follow list: " + x + "\n"
					logNprint(toprint)
				except:
					logNprint("Error Occured. Unfollow failed \n")
		except:
			logNprint("Error checking follow \n")
		time.sleep(5)
		

def checkFollow(item):

	print("Am following?: " + item['user']['screen_name'] + " - " + str(item['user']['following']))
	if str(item['user']['following']) == "False":
		text = item['text']
		user = item['user']
		screen_name = user['screen_name']
		id = user['id']

		if any(string in text.lower() for string in follow_key):
			try:
				r = api.request('friendships/create', {'id': id})
				
				toprint = "Following: " + screen_name + "\n"
				logNprint(toprint)
				#print ("Following: " + screen_name + "\n")
				
				today = datetime.datetime.now()
				now = today.date()
				
				followlist.append(str(id) + "_" + str(now))

				f_fol = open(track_file_path + "followlist", 'a')
				f_fol.write(str(id) + "_" + str(now) + "\n")
				f_fol.close()
			except:
				logNprint("Error occured. Follow failed")
	else:
		toprint = "Already following user: " + item['user']['screen_name']
		logNprint(toprint)
		#print("Already following user: " + item['user']['screen_name'])

def checkLike(item):

	text = item['text']
	id = item['id']	
	shortened = textwrap.shorten(text, width = 50)

	if any(string in text.lower() for string in fav_key):
		try:
			r = api.request('favorites/create', {'id': id})
			toprint = "Liked: " + shortened + "\n"
			logNprint(toprint)
		except:
			logNprint("Erorr occured, Like failed")


def processQueue():

	while len(tweet_queue) > 0:
		#retweet
		tweet = tweet_queue.pop()
		
		toprint = "******************" + "Queue Length: " + str(len(tweet_queue)) + "*************************"
		logNprint(toprint)
		
		text = tweet['text']
		text = text.replace("\n"," ")
		toprint = "Retweeting: " + tweet['text'] + "\n"
		logNprint(toprint)

		try:
			r = api.request('statuses/retweet/:' + str(tweet['id']))
		except:
			logNprint("Error occured. Retweet failed \n")
		
		#check for follow request
		checkFollow(tweet)
		#check for like/favorite request
		checkLike(tweet)
		
		
		toprint = "*******************************************"
		logNprint(toprint)

		
		time.sleep(20)
	
def botCheck(item):
	user_data = item['user']
	user_id = user_data['id']
	user_screen_name = user_data['screen_name']
	screen_name_lowercase = user_screen_name.lower()
	
	#for each case of bot keywords
	for string in bot_check:
		#if any seem like bots
		if string in screen_name_lowercase:
			#add the user ID for that twitter account to the do not follow list
			donotfollow.append(user_id)
			
			toprint = "Bot Found! Added to do not follow list \n"
			logNprint(toprint)

			
			f_dnf = open(track_file_path + "donotfollow", 'a')
			f_dnf.write(str(user_id) + "\n")
			f_dnf.close()

	
def getTweets():

	for search_query in search_queries:
		try:
			r = api.request('search/tweets', {'q':search_query, 'result_type':"mixed", 'count':count_per_Search})
			
			toprint = "Getting results for " + search_query + "\n"
			logNprint(toprint)

			
			for item in r:
				

				#collect the tweet data we need based on it if is a retweet or not
				#tweet data
				#if there is a retweet_status it is a retweeted tweet
				if 'retweeted_status' in item:
					toprint = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ \n Retweeted item \n"
					logNprint(toprint)

					
					original_item = item['retweeted_status']#pulls data from original tweet, not the retweet
					#original user of the tweet data
					original_user_data = original_item['user']
					original_screen_name = original_user_data['screen_name']
					original_user_id = str(original_user_data['id'])
					
					#original tweet data
					original_tweet_id = str(original_item['id'])
					original_tweet_text = original_item['text']
					original_have_rted = original_item['retweeted']
					original_have_fvted = original_item['favorited']
					
					botCheck(original_item)
					
					if not original_user_id in donotfollow:
					
						if not original_tweet_id in ignorelist:
							toprint = "Okay to process retweet \n"
							logNprint(toprint)

							ignorelist.append(original_item)
							tweet_queue.append(original_item)
							
							print(" Added to queue. Added to ignore list \n")
							
							f_ign = open(track_file_path + "ignorelist", 'a')
							f_ign.write(str(original_tweet_id) + "\n")
							f_ign.close()
						else:
							toprint = "Ignored: " + str(original_tweet_id) + "\n"
							logNprint(toprint)
							
							ignorelist.append(item['id'])
							
							f_ign = open(track_file_path + "ignorelist", 'a')
							f_ign.write(str(original_tweet_id) + "\n")
							f_ign.close()
							
					else:
						toprint = str(original_user_id) + " On do not follow list \n"
						logNprint(toprint)

							
					time.sleep(5)
						
					
				else:
					toprint = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ \n New item \n"
					logNprint(toprint)
					
					user_data = item['user']# user data in json forma
					screen_name = user_data['screen_name']#screen name of the specific user who tweeted
					user_id = str(user_data['id'])# user ID pulled from user data
					
					#tweet data
					text = item['text'] # text of the tweet
					tweet_id = str(item['id'])#id for the specific tweet
					have_rted = item['retweeted']#this object holds a true or false value
					have_fvted = item['favorited']#this object holds true or false value

					botCheck(item)
					
					if not user_id in donotfollow:

						if not tweet_id in ignorelist:
							toprint = "Okay to process \n"
							logNprint(toprint)

							tweet_queue.append(item)
							ignorelist.append(tweet_id)
							
							print(" Added to queue. Added to ignore list \n")
							
							f_ign = open(track_file_path + "ignorelist", 'a')
							f_ign.write(str(tweet_id) + "\n")
							f_ign.close()
						else:
							toprint = "Ignored: " + str(tweet_id) + "\n"
							logNprint(toprint)

					else:
						toprint = str(original_user_id) + " On do not follow list \n"
						logNprint(toprint)

							
					time.sleep(5)
		except:
			logNprint("Error occured during get tweets")

	
#Start of the main loop
while (True):
	toprint = "########################Scanning for Tweets \n"
	logNprint(toprint)
	#print("########################Scanning for Tweets \n")
	getTweets()
	
	time.sleep(7) #Sleep to avoid rate limit
	toprint = "########################Processing Tweet Queue \n"
	logNprint(toprint)
	#print("########################Processing Tweet Queue \n")
	
	processQueue()
	
	toprint = "########################Running Unfollow Bot \n"
	logNprint(toprint)

	unFollowBot()
	
	time.sleep(7) #sleep to avoid rate limiting
	print("Printing ignore list for testing \n")
		
	os.remove(track_file_path + "followlist")
	
	f_fol = open(track_file_path + "followlist", 'a')
	for x in followlist:
		f_fol.write(x + "\n")

	logNprint("\n")
	print("Okay to exit. Will continue shortly.")
	f_fol.close()
	
	time.sleep(60)