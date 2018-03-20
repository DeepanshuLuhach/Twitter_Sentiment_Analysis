from django.shortcuts import render
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError

import os
import requests

import tweepy
from textblob import TextBlob

### For Logging purposes to console.. disable in production
# import logging
# logger = logging.getLogger(__name__)

def twitterHero(data,size):
    consumer_key='hRtjBC96kuPWauOdA8PhIstWf'
    consumer_secret='Yr3OYXjGxuHKP9jZzLfVmGPgzOp7B7YVVzGT7QI26HSs1ylurs'
    access_token='787583680948514816-ahVdtUZmzh6qij2PgrcslGecI48SPs1'
    access_token_secret='hpcSbQt9AgsoTUsXmsqyC9utlvWemNU3bn2nJnJqlEsk4'
    auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)

    api=tweepy.API(auth)

    S=[]
    counter=[0,0,0] # positive, negative, neutral
    for tweet in tweepy.Cursor(api.search, q=data, rpp=100, count=20, result_type="recent", include_entities=True, lang="en").items(size):
        # logger.log(100,tweet)  # MASSIVE DATA DUMP for debugging
        analysis=TextBlob(tweet.text)
        if analysis.sentiment.polarity > 0:
            print(counter[0])
            res='positive'
            counter[0]+=1
        elif analysis.sentiment.polarity == 0:
            res='neutral'
            counter[2]+=1
        else:
            res='negative'
            counter[1]+=1
        S.append((tweet.text,analysis.sentiment,res,tweet.user.name,tweet.user.profile_image_url_https,tweet.user.screen_name))
    size=counter[0] + counter[1] + counter[2]
    positivePer=(counter[0])*100
    negativePer=(counter[1])*100
    neutralPer=(counter[2])*100
    print(counter[0]/size)
    print(positivePer)
    print(size)
    positivePer=positivePer/size
    negativePer=negativePer/size
    neutralPer=neutralPer/size
    print(positivePer)
    S.append((positivePer,negativePer,neutralPer))
    return S


def index(request):
    return render(request,'website/home.html',{})


def form_data(request):
    try:
        data=request.POST['q']
        size=int(request.POST['size'])
    except MultiValueDictKeyError:
        data='Rajasthan'
        size=50
    if data=='':
        data='Rajasthan'
    S=twitterHero(data,size)
    # logger.log(100,"Called function.")
    posPer,negPer,ntrPer=S[-1][0],S[-1][1],S[-1][2]
    del S[-1]
    return render(request,'website/index.html',{'data':S,'search':data,'posPer':posPer,'negPer':negPer,'ntrPer':ntrPer})
