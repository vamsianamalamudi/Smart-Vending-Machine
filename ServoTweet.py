from __future__ import absolute_import, print_function

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import time
import RPi.GPIO as GPIO

SearchTag = 'atria' # Tweet to be searched in twitter API 
PlaceType = 'poi'
PlaceName = 'Atria' # Place where you have to search for tweets

#Connections

LED = 21 #Connection for led
ServoPin = 12 #Connection for servo motor
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED, GPIO.OUT)
GPIO.setup(ServoPin, GPIO.OUT)
GPIO.output(LED, GPIO.LOW)
Servo = GPIO.PWM(ServoPin, 50)
Servo.start(7.5)

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key="wJx8Dzc4af4cWKM1fRrpVeMva"
consumer_secret="NhaQZsX7scYc8mSzvERVb8h8MqY4X672NaeFLey7CwbqBhF4tv"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="3066036252-AlnQ9jAbqIWHoUGotPb2tOoSZwthltBjRhZZtBK"
access_token_secret="EVFmjqhnWbqW8sVBvr5UVATwb4jVz3YNW6UJ3iKCHb9Dt"

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        #print(data)
        jsondata = json.loads(data)
        for item in jsondata['entities']['hashtags']:
            if item['text']==SearchTag:
                print ("Hashtag Detected!")
           
        if jsondata['place'] != None and jsondata['place']['place_type']==PlaceType and jsondata['place']['name']==PlaceName:
            print ("Vending...!")
            GPIO.output(LED, GPIO.LOW)
            Servo.ChangeDutyCycle(12.5)
            time.sleep(3)
            GPIO.output(LED, GPIO.HIGH)
            Servo.ChangeDutyCycle(7.5)
            #print (jsondata['coordinates'])
            if jsondata['coordinates'] != None:
                print ("Latitude: " + str(jsondata['coordinates']['coordinates'][0]) + "\tLongitude: " + str(jsondata['coordinates']['coordinates'][1]))
            else:
                print ("Unable to fetch exact coordinates")
        elif jsondata['place'] != None:
            print ("Place not matched!")
            print ("Detected Place Type: " + str(jsondata['place']['place_type'] + "\t Place Name: " + str(jsondata['place']['name'])))
        else:
            print ("Couldn't locate the place! Please check if you are tagging the location correctly.")
        return True

    def on_error(self, status):
        Servo.stop()
        GPIO.cleanup()
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=[SearchTag])
