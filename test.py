#!/usr/bin/env python
# -*- coding: utf-8 -*-

# lmd_test user id: 784831043819802624

import tweepy, json, sys

config_file = str(sys.argv[1])
fin = open(config_file)
config = json.load(fin)
fin.close()

MY_USER_ID = config['USER_ID']
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
        if 'retweeted_status' in status._json:
            pass
        else:
            if status.user.id == MY_USER_ID:
                if MY_USER_ID in map(lambda x: x['id'], status.entities['user_mentions']):
                    response = '@{} nice to hear from you'.format(status.user.screen_name)
                else:
                    response = '@{} hello'.format(status.user.screen_name)
                api.update_status(response, in_reply_to_status_id = status.id)
                print("\nNew tweet:")
                print(status._json['text'])
                print(json.dumps(status._json, indent = 4))

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

botStreamListener = BotStreamListener()
botStream = tweepy.Stream(auth = auth, listener = botStreamListener)
botStream.filter(track = ['clinton trump'])
