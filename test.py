#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy, json, sys

config_file = str(sys.argv[1])
fin = open(config_file)
config = json.load(fin)
fin.close()

CONSUMER_KEY = config['CONSUMER_KEY']
CONSUMER_SECRET = config['CONSUMER_SECRET']
ACCESS_KEY = config['ACCESS_KEY']
ACCESS_SECRET = config['ACCESS_SECRET']
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.secure = True
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

class BotStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print("\nNew tweet:")
        print(status._json['text'])
        print(status._json.keys())

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

botStreamListener = BotStreamListener()
botStream = tweepy.Stream(auth = auth, listener = botStreamListener)
botStream.filter(track = ['clinton trump'])
