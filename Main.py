#!/usr/bin/env python
# coding: utf-8

# In[12]:


import tweepy
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import credantials
import pymongo
from pymongo import MongoClient
from mysql import connector
from datetime import datetime,timedelta
import pandas as pd
import multiprocessing
from textblob import TextBlob


# In[13]:


try:
    mydb=connector.connect(
        host="localhost",
        user="root",
        password="",
        database="CoronaTweets",
        charset='utf8'
    )
    print("connected")
except Exception as e:
    print("Not Connect to Database")


# In[14]:


mycursor=mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS CoronaTweetData (id_str VARCHAR(255),created_at VARCHAR(255),tweet_text VARCHAR(255),polarity VARCHAR(255),subjectivity VARCHAR(255),user_created_at VARCHAR(255),user_location VARCHAR(255),user_description VARCHAR(255),user_followers_count VARCHAR(255),total_favorites VARCHAR(255),total_retweet VARCHAR(255))")
mydb.commit()
mycursor.close()


# In[15]:


import re
def Preprocesstext(text):
    if text:
        return (' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|([RT])"," ",text).split()))
    else:
        return None


# In[ ]:





# In[16]:


class CronaStreamListner(StreamListener):
    
    def on_status(self,status):
        try:
            id_str=status.id_str
            created_at=status.created_at
            tweet_text=Preprocesstext(status.text)
            sentiment=TextBlob(tweet_text).sentiment
            if(sentiment.polarity<0):
                polarity=-1
            elif(sentiment.polarity==0):
                polarity=0
            else:
                polarity=1
            subjectivity=sentiment.subjectivity
            user_created_at=status.user.created_at
            user_location=status.user.location
            user_description=status.user.description
            user_followers_count=status.user.followers_count
            total_favorites=status.favorite_count
            total_retweet=status.retweet_count
            if mydb.is_connected():
                mycursor=mydb.cursor()
                sql="INSERT INTO CoronaTweetData (id_str,created_at,tweet_text,polarity,subjectivity,user_created_at,user_location,user_description,user_followers_count,total_favorites,total_retweet) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                val=(id_str,created_at,tweet_text,polarity,subjectivity,user_created_at,user_location,user_description,user_followers_count,total_favorites,total_retweet)
                mycursor.execute(sql,val)
                mydb.commit()
                mycursor.close()
                
            
            
        except Exception as e:
            print(e)

        
    def on_error(self,status_code):
        if status_code==420:
            return False


# In[17]:


auth=OAuthHandler(credantials.CONSUMER_KEY,credantials.CONSUMER_SECRET)
auth.set_access_token(credantials.ACCESS_KEY,credantials.ACCESS_SECRET)
api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)


# In[18]:


mystreamer=CronaStreamListner()
Stream=tweepy.Stream(auth=api.auth,listener=mystreamer)
Stream.filter(languages=["en"],track=["coronavirus","2019nCoV","COVID19"])


# In[19]:


time_now=datetime.utcnow()
time_10min=timedelta(hours=0,minutes=10)
time_itnterval=time_now-time_10min
time_itnterval=time_itnterval.strftime('%Y-%m-%d %H:%M:%S')
time_itnterval


# In[ ]:




