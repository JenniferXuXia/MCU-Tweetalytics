import tweepy
import config
from textblob import TextBlob
import pandas as pd
import plotly.express as px

# Tweepy authentication
auth = tweepy.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


# DEFINING FUNCTIONS: get polarity functions

# get polarity function using standard search tweet function
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


# get polarity function using search_full_archive function
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


# MODIFYING/UPDATING DATASET
# modify existing mcu_properties csv file by creating columns for search_full_archive parameters,
# and column for polarity

df = pd.read_csv(r"C:\Users\jennifer\Documents\csv\mcu_properties.csv")
from_date = []
to_date = []
search_phrase = []

for i in df.index:
    # create fromDate parameter of Tweepy search function
    from_date.append((df["Release Date"][i].replace(" ", "")) + "0000")

    # for release date, create list by converting string date into a list of integers in [year, month, day] format
    release_date_list = df["Release Date"][i].split(" ", 3)

    # create toDate parameter of Tweepy search function
    toYear = int(release_date_list[0])
    toMonth = int(release_date_list[1]) + 1
    if toMonth > 12:
        toMonth -= 12
        toYear += 1

    toMonth = str(toMonth)
    if len(toMonth) == 1:
        toMonth = "0" + toMonth

    to_date_str = str(toYear) + str(toMonth) + release_date_list[2] + "0000"
    to_date.append(to_date_str)

    new_phrase = "(" + df["Search Phrase"][i] + ") lang:en"
    search_phrase.append(new_phrase)

df.insert(2, "From Date", from_date, True)
df.insert(3, "To Date", to_date, True)
df.drop(["Search Phrase"], axis=1)
df["Search Phrase"] = search_phrase

print(df["Search Phrase"])

# CALCULATE POLARITY FOR EACH MCU PROPERTY AND ADDS TO DATAFRAME

# polarity = []
# for i in df.index:
#     this_polarity = dated_polarity(df["Search Phrase"][i], df["From Date"][i], df["To Date"][i])
#     polarity.append(this_polarity)

# df.insert(polarity)
# print(df.head())

# SAVING DATAFRAME

# df.to_pickle(path and filename)

# RETRIEVE DATAFRAME

# df = pd.read_pickle(file_name)

# DATA VISUALIZATION (IDEAS)
# sentiment polarity bar graph across all mcu properties
# average polarities for each phase bar graph
# pie chart with worst polarities across phases, quartiles
# scatter plot of queryTopic #marvel across time
# compare polarities with critic/audience critic ratings
