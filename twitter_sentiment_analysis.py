import time
import sys
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
from textblob import TextBlob
import matplotlib.pyplot as plt
import re


def calctime(a):
    return time.time()-a

positive=0
negative=0
neutral=0
compound=0
count=0

#Interactive Plot
initime=time.time()
plt.ion()


searchTerm = input("enter keyword or hashtag to search: ")

#Authorisation credentials 
ckey='2JWW2dgGs7bL01Bv7AKujaNxF'
csecret='fpMRwYIZ7hNrhPsXimx6N07iHuN9rRs8VD30JdRznjJU3xDzz6'
atoken='1252901996979355648-F4Q3YGrxyfBS3F5XvntYGjluYW5IcU'
asecret='YWL62gJXAJpum3CTNSFtg0JeDueLPOPzX6kA7K0IBqLSY'


#stream live tweets
class listener(StreamListener):
    
    def on_data(self,data):
        global initime
        t=int(calctime(initime))
        all_data=json.loads(data)
        non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
        tweet=all_data["text"].translate(non_bmp_map)
        tweet=" ".join(re.findall("[a-zA-Z]+", tweet))
        blob=TextBlob(tweet.strip())
        
        global positive
        global negative
        global neutral
        global compound  
        global count
        
        #calculate sentiment for each sentence
        count=count+1
        senti=0
        for sen in blob.sentences:
            senti=senti+sen.sentiment.polarity
            if sen.sentiment.polarity >0:
                positive=positive+sen.sentiment.polarity 
            elif sen.sentiment.polarity==0:
                 neutral=neutral+sen.sentiment.polarity
            else:
                negative=negative+sen.sentiment.polarity  
        compound=compound+senti        
        print('COUNT: ',count)
        print('TWEET: ',tweet.strip())
        if senti>0:
            print('SENTIMENT: ',senti,'positive')
        elif senti<0:
            print('SENTIMENT: ',senti,'negative')
        else:
            print('SENTIMENT: ',senti,'neutral')
        print('TIME',t)
        print("TOTAL SENTIMENT PER SENTENCE")
        print('Positive sentiment: ',str(positive) + ' ' + 'Negative sentiment: ', str(negative) + ' ' +
              'Neutral sentiment: ', str(neutral) + ' ' +'Compound sentiment: ', str(compound))
        print('________________________________________________________________________________')

        #Plotting graph
        plt.axis([ 0,150 , -30,30])
        plt.xlabel('Time')
        plt.ylabel('Sentiment')
        plt.plot([t],[positive],'go',[t] ,[negative],'ro',[t],[neutral],'yo',[t],[compound],'bo')
        plt.show()
        plt.pause(0.001)
        if count==200:
            return False
        else:
            return True
        
    def on_error(self,status):
        print(status)

#Authorisation
auth=OAuthHandler(ckey,csecret)
auth.set_access_token(atoken,asecret)
twitterStream=Stream(auth, listener(count))
twitterStream.filter(track=[searchTerm],languages=["en"])
