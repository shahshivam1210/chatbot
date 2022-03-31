import pyttsx3
import speech_recognition as sr 
import datetime
import wikipedia
import sys
import psutil
import os
from youtube_search import YoutubeSearch
import re
import long_responses as long

# to make speak function

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
#print(voices)
engine.setProperty('rate', 180)
# to make battery percentage
battery = psutil.sensors_battery()
current_battery = battery.percent

def speak(text):
    engine.say(text)
    engine.runAndWait()


def takeCammand():

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening....")
        r.energy_threshold = 300 
        r.pause_threshold = 5
        audio = r.listen(source, timeout=7, phrase_time_limit=7)

    try:
        print("recognizing....")
        query = r.recognize_google(audio, language='hi')
        #print(f" user said that {query}")

    except Exception as e:
        return 'none'

    return query


query = takeCammand().lower()
print(query)
if 'मेरा नाम शिवम कुमार साह है' in query:
    print("its okay")