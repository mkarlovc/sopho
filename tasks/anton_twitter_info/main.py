#!/usr/bin/python
import os, sys
import json
import timeit
import operator

def is_retweet(text):
    if text[0:2] == "RT":
        return True
    else:
        return False

start_time = timeit.timeit()

# Open a file
path = r"/media/mario/My Book/mario/sopho/twitter/all"
dirs = os.listdir( path )

# This would print all the files and directories
filelist = []
for file in dirs:
    fullpath = path+"/"+file
    filelist.append(fullpath)

# number of retweets a tweet ha
tweets = {}
# user id who initiated the tweet
tweets_user = {}
# tweet retweet user with max followers
tweets_maxfu = {}
# N of retweet of user with max followers
tweets_maxu = {}

for file in filelist:
    print file
    with open(file, "r") as ins:
        for line in ins:
            try:
                j = json.loads(line)
                if j.has_key('text'):
                    text = j['text']
                    if is_retweet(text) == True:
                        text = text.split(': ')[1]
                        tweets[text] = tweets[text] + 1
                        max_temp = tweets_maxfu[text]
                        followers = int(j["user"]["followers_count"])
                        if followers > max_temp:
                             tweets_maxfu[text] = followers
                             tweets_maxu[text] = int(tweets[text])
                    else:
                        tweets[text] = 0
                        tweets_maxfu[text] = 0
                        tweets_maxu[text] = 0
                        user = {}
                        user["user_id"] = j["user"]["id_str"]
                        user["user_followers"] = j["user"]["followers_count"]
                        user["tweet_id"] = j["id_str"]
                        user["tweet_date"] = j["created_at"]
                        user["tweet_date_ms"] = j["timestamp_ms"] 
                        tweets_user[text] = user
            except:
                pass

# sort tweets by number of retweets
tweets = sorted(tweets.items(), key=operator.itemgetter(1))
tweets.reverse()

# write ti screen
for i,t in enumerate(tweets[0:100]):
    print(str(tweets_user[t[0]]["tweet_id"]),str(t[1]),str(tweets_user[t[0]]["user_followers"])\
,str(tweets_user[t[0]]["tweet_date_ms"]),str(tweets_user[t[0]]["tweet_date"]),tweets_maxfu[t[0]]\
,tweets_maxu[t[0]])

# write to file
f = open('retweet_maxfu.txt','w')
for i,t in enumerate(tweets[0:10]):
    f.write(str(tweets_user[t[0]]["tweet_id"])+","+str(t[1])+","+str(tweets_user[t[0]]["user_followers"])+","+\
str(tweets_user[t[0]]["tweet_date_ms"])+","+str(tweets_user[t[0]]["tweet_date"])+","+\
str(tweets_maxfu[t[0]])+","+str(tweets_maxu[t[0]])+"\r\n")
f.close()

end_time = timeit.timeit()

print start_time - end_time

def is_retweet(text):
    if text[0:2] == "RT":
        return True
    else:
        return False
