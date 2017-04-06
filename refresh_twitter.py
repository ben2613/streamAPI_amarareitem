from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import json
import urllib.request
import sys
import re
import webbrowser

class StdOutListener(StreamListener):
    def on_data(self, data):
        tweet = json.loads(data)
        print('--------------------------------------------------')
        print(tweet['user']['screen_name'])
        print(tweet['text'])
        self.auto_open(tweet)
        return True

    def on_error(self, status):
        print(status)
        
    def auto_open(self, tweet):
        text = tweet['text']
        if 'けものフレンズBD付オフィシャルガイドブック' in text and not '終了' in text:
            urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', tweet['text'])
            for url in urls:
                webbrowser.open(url)

if __name__ == '__main__':
    if len(sys.argv) is not 1:
        with open('example.json', encoding='utf-8') as f:
            tweet = json.loads(f.read())
        print(tweet['text'])
        StdOutListener.auto_open('1',tweet)
        exit()

    #Variables of OAuth
    with open('credential') as f:
        cred = dict(line.split('=') for line in f.read().splitlines())

    l = StdOutListener()
    auth = OAuthHandler(cred['api_key'], cred['api_secret'])
    auth.set_access_token(cred['access_token'], cred['access_token_secret'])
    stream = Stream(auth, l)
    # twitter id of amarareitem
    stream.filter(follow=['471956654'])
