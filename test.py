#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy, json, sys
import wit
import pprint

config_file = str(sys.argv[1])
fin = open(config_file)
config = json.load(fin)
fin.close()

CONSUMER_KEY = config['CONSUMER_KEY']
CONSUMER_SECRET = config['CONSUMER_SECRET']
ACCESS_KEY = config['ACCESS_KEY']
ACCESS_SECRET = config['ACCESS_SECRET']
WIT_AI = config['WIT_AI']
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.secure = True
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
wit_client = wit.Wit(access_token=WIT_AI)
test_account = 784989766685044736

class BotStreamListener(tweepy.StreamListener):
	def on_status(self, status):
		print("\nNew tweet:")
		print(status.text)
		print("Checking if I should reply")
		global wit_client
		resp = wit_client.message(status.text)
		try:
			intent = resp['entities'].keys()[0]
			if intent=="no_reply":
				print "I would not have replied"
			elif intent=="email_apology":
				reply = "Have you read this? https://www.washingtonpost.com/news/post-politics/wp/2015/09/08/hillary-clinton-apologizes-for-e-mail-system-i-take-responsibility/"
				response = '@{} {}'.format(status.user.screen_name, reply)
				if status.user.id == test_account:
					print "Actually posting!"
					api.update_status(response, in_reply_to_status_id = status.id)
				print "I replied with ", response
				pprint.pprint(status)
		except:
			print "Error!"
			pass

	def on_error(self, status_code):
		if status_code == 420:
			#returning False in on_data disconnects the stream
			return False

botStreamListener = BotStreamListener()
botStream = tweepy.Stream(auth = auth, listener = botStreamListener)
botStream.filter(track = ['hillary apologized emails'])



def reply_function(tweet_content):
    return 'You said {}'.format(tweet_content)

class BotStreamListener(tweepy.StreamListener):
    # def __init__(self, reply_function):
    #     self.reply_function = reply_function

    def on_status(self, status):
        if 'retweeted_status' in status._json:
            pass
        else:
            if status.user.id == my_user_id:
                user_mentions = filter(lambda x: x['id'] == my_user_id, status.entities['user_mentions'])
                if len(user_mentions) > 0:
                    username = '@{}'.format(user_mentions[0]['screen_name'])
                    tweet_content = string.replace(status.text, username, '')
                else:
                    tweet_content = status.text
                response = '@{} {}'.format(status.user.screen_name, reply_function(tweet_content))
                api.update_status(response, in_reply_to_status_id = status.id)
                print("\nNew tweet:")
                print(status._json['text'])
                print(json.dumps(status._json, indent = 4))
