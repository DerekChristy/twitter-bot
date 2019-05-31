import tweepy
import requests
import time
from os import environ

print('this is my twitter bot')

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_SECRET = environ['ACCESS_SECRET']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

url = "http://randomuselessfact.appspot.com/random.json?language=en"
id_file = "prev-ids.txt"

def get_last_mention_id(file):
    f_read = open(file, 'r')
    last_mention_id = int(f_read.read().strip())
    f_read.close()
    return last_mention_id

def set_last_mention_id(last_mention_id, file):
    w_file = open(file, 'w')
    w_file.write(str(last_mention_id))
    w_file.close()
    return

while True:
    prev_id = get_last_mention_id(id_file)
    #print("PREV ID: " + str(prev_id))
    mentions = api.mentions_timeline(prev_id)
    
    for mention in mentions:
        #print("CUR ID: " + str(mention.id))
        set_last_mention_id(mention.id, id_file)
        if((mention.text).lower().find("random-fact") != -1):
            obj = requests.get(url)
            data = obj.json()
            fact = data['text']
            api.update_status('@' + mention.user.screen_name + " here is your fact:-\n" + fact)
            print('@' + mention.user.screen_name + " here is your fact:-\n" + fact)
    time.sleep(60)
