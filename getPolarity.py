import tweepy
import config
from textblob import TextBlob
import pandas as pd
import plotly.express as px

auth = tweepy.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

def polarity(query):
    tweets = [tweet for tweet in tweepy.Cursor(api.search_tweets,
                                               q=query, lang="en", result_type="mixed", count=1000).items(1000)]
    sum_polarity = 0.0
    count = 0
    for tweet in tweets:
        analysis = TextBlob(tweet.text)
        sum_polarity += analysis.polarity
        count += 1

    return sum_polarity / count


# date format is YYYYMMDDHHMM (year, month, day, hour, minute)
def dated_polarity(query, from_date, to_date):
    tweets = [tweet for tweet in tweepy.Cursor(api.search_full_archive,
                                               label=config.FULL_ARCHIVE, query=query,
                                               fromDate=from_date, toDate=to_date).items(100)]
    sum_polarity = 0.0
    count = 0
    for tweet in tweets:
        analysis = TextBlob(tweet.text)
        sum_polarity += analysis.polarity
        # check tweet validity
        if count < 10:
            print(tweet)
            print(analysis.polarity)
        count += 1

    return sum_polarity / count
    print("Count: " + count)