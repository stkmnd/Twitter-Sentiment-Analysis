from itertools import count
from tokenize import PlainToken
from turtle import color
import tweepy
from textblob import TextBlob
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

def cleanText(text):
    # Remove Twitter handles
    text = re.sub(r'@[A-Za-z0-9_\']+', '', text)
    # Remove hashtags
    text = re.sub(r'#[A-Za-z0-9]', '', text)
    # Remove retweets
    text = re.sub(r'RT[\s]+', '', text)
    # Remove hyperlinks
    text = re.sub(r'https?:\/\/\S+', '', text)

    return text

def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity

def getPolarity(text):
    return TextBlob(text).sentiment.polarity

def getAnalysis(score):
    if score < 0:
        return 'Negative'
    if score > 0:
        return 'Positive'
    return 'Neutral'

def getPositiveTweets(df):
    """
    Print the positive tweets of a Twitter user
    and return the number of positive tweets.
    """
    count = 1
    for i in range(df.shape[0]):
        if df['Analysis'][i] == 'Positive':
            print(str(count) + ') ' + df['Tweets'][i])
            print()
            count += 1
    return count

def getNegativeTweets(df):
    """
    Print the negative tweets of a Twitter user
    and return the number of negative tweets.
    """
    count = 1
    for i in range(df.shape[0]):
        if df['Analysis'][i] == 'Negative':
            print(str(count) + ') ' + df['Tweets'][i])
            print()
            count += 1
    return count

def getNeutralTweets(df):
    """
    Print the neutral tweets of a Twitter user
    and return the number of neutral tweets.
    """
    count = 1
    for i in range(df.shape[0]):
        if df['Analysis'][i] == 'Neutral':
            print(str(count) + ') ' + df['Tweets'][i])
            print()
            count += 1
    return count

username = input("Please enter the Twitter handle: ")
numberOfTweets = input("Please enter the number of tweets fetched: ")

# Developer keys and tokens have been removed for security purposes
customerKey = "XXX"
customerSecret = "XXX"
accessToken = "XXX"
accessTokenSecret = "XXX"

# Twitter API Authentication
authenticate = tweepy.OAuthHandler(customerKey, customerSecret)
authenticate.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(authenticate)

# Retrieve the posts of the Twitter user
posts = api.user_timeline(screen_name=username, count=numberOfTweets, tweet_mode='extended')
df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])

df['Tweets'] = df['Tweets'].apply(cleanText)
df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
df['Polarity'] = df['Tweets'].apply(getPolarity)
df['Analysis'] = df['Polarity'].apply(getAnalysis)

plt.title('Sentiment Analysis')
plt.xlabel('Sentiment')
plt.ylabel('Count')
df['Analysis'].value_counts().plot(kind='bar')
plt.show()
