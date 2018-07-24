#!/usr/bin/env python
#-*- coding: utf-8 -*-
import json
import time
import tweepy
import pymongo
import pandas as pd


class TwitterData:
    def __init__(self, access_token_key, access_token_secret, consumer_key, consumer_secret):
        self.access_token_key = access_token_key
        self.access_token_secret = access_token_secret
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret       

    def searchUser(self, document,dbName,collection):
        conn = pymongo.MongoClient('mongodb://localhost:27017')
        db = conn[dbName]
        datos = db.create_collection(collection)
        sleep_time = 1.01
        

        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token_key,self.access_token_secret)
        api = tweepy.API(auth)
        #print api
        #sleep_time = 1.01
        data = pd.read_csv(document,header=0)
        users = list(data.screen_name)
        usersList = []
        existsList = []
        for user in users:
            #print user
            #print '\n'
            try:
                infoUser = api.get_user(user)
                usersList.append(user)
                existsList.append('True')
                datos.insert({'screen_name': user, 'code': 200})
                time.sleep(sleep_time)
                #print user+': True'
            except Exception as e:
                print e
                if e[0][0]['code'] in [63,50]:
                    usersList.append(user)
                    existsList.append('False')
                    datos.insert({'screen_name': user, 'code': e[0][0]['code']})
                    #print user+': False'
                    time.sleep(sleep_time)
                elif e[0][0]['code'] >= 400:
                    print e
                    break

#        df = pd.DataFrame({'screen_name': usersList, 'exist': existsList})
#        df.to_csv('Bots-'+document, index=False)
       

access_token_key = 'XXXX-XXXX'
access_token_secret = 'XXXX-XXXX'
consumer_key = 'XXXX-XXXX'
consumer_secret = 'XXXX-XXXX'


twitter = TwitterData(access_token_key, access_token_secret, consumer_key, consumer_secret)
tw3k = twitter.searchUser('accounts.csv','brexit','accounts3k')
time.sleep(150)
tw = TwitterData(access_token_key, access_token_secret, consumer_key, consumer_secret)
twAll = twitter.searchUser('all_accounts.csv','brexit','allAccounts')


