#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy, json, sys
import wit
import pprint

config_file = "config_hillipedia.json"
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


def strip_non_ascii(text):
	return ''.join([i if ord(i) < 128 else '' for i in text])


class BotStreamListener(tweepy.StreamListener):
	def on_status(self, status):
		print("\nNew tweet:")
		print(status.text)
		print("Checking if I should reply")
		if 'retweeted_status' in status._json:
			print "Hillipedia doesn't reply to re-tweets"
			return
		global wit_client
		resp = wit_client.message(status.text)
		try:
			intent = resp['entities'].keys()[0]
			if intent=="no_reply":
				print "I would not have replied"
			elif intent=="email_apology":
				reply = "Actually..have you read this? https://www.washingtonpost.com/news/post-politics/wp/2015/09/08/hillary-clinton-apologizes-for-e-mail-system-i-take-responsibility/ " + status.text.replace("@","")
				response = '@{} {}'.format(status.user.screen_name, reply)
				print "Actually posting!"
				api.update_status(strip_non_ascii(response.encode("utf-8")), in_reply_to_status_id = status.id)
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
