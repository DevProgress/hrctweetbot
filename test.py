#!/usr/bin/env python
# -*- coding: utf-8 -*-

# lmd_test user id: 784831043819802624

import tweepy, json, sys, string

config_file = str(sys.argv[1])
fin = open(config_file)
config = json.load(fin)
fin.close()

test_account = 784989766685044736

my_user_id = config['user_id']
consumer_key = config['consumer_key']
consumer_secret = config['consumer_secret']
access_key = config['access_key']
access_secret = config['access_secret']
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.secure = True
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

def reply_function(tweet_content):
    return 'You said {}'.format(tweet_content)

class BotStreamListener(tweepy.StreamListener):
    # def __init__(self, reply_function):
    #     self.reply_function = reply_function

    def on_status(self, status):
        if 'retweeted_status' in status._json:
            pass
        else:
            if status.user.id == test_account:
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

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False


botStreamListener = BotStreamListener()#reply)
botStream = tweepy.Stream(auth = auth, listener = botStreamListener)
botStream.filter(track = ['clinton trump'])
