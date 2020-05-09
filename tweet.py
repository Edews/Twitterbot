import RPi.GPIO as GPIO
import time
import tweepy

# coding=utf-8

#here is where you need to add your own keys from the Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)

api = tweepy.API(auth)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#These are the three GPIO pins  my LED's are connected to
GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)

#This is where I specify which hashtags I want to track and which color I want them on. Could've named them better, but since I'm working with color, this was more fun.
blue = "covid19"
green = "corona"
red = "quarantine"

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
		for i in range(len(status.entities.get('hashtags'))): #for every tweet, it checks all hashtags to see if it matches any of the three we're looking for
			if (status.entities.get('hashtags')[i].get('text')) == blue:
				print status.author.screen_name +  " just used the hashtag " + (status.entities.get('hashtags')[i].get('text'))
				GPIO.output(22,GPIO.HIGH) #LED goes blink
				time.sleep(0.1) #LED stays blink
				GPIO.output(22,GPIO.LOW) #LED goes blonk

			elif (status.entities.get('hashtags')[i].get('text')) == green:
				print status.author.screen_name + " just used the hashtag " + (status.entities.get('hashtags')[i].get('text'))
				GPIO.output(27,GPIO.HIGH)
				time.sleep(0.1)
				GPIO.output(27,GPIO.LOW)

			elif (status.entities.get('hashtags')[i].get('text')) == red:
				print status.author.screen_name + " just used the hashtag " + (status.entities.get('hashtags')[i].get('text'))
				GPIO.output(17,GPIO.HIGH)
				time.sleep(0.1)
				GPIO.output(17,GPIO.LOW)


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

#here is where the filter actually starts. You can change it to either a simple string for keywords, or add a @ to find whatever someone tweeted to.
myStream.filter(track=['#'+blue, '#'+green, '#'+red])
