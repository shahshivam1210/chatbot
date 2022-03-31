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
        query = r.recognize_google(audio, language='en-in')
        #print(f" user said that {query}")

    except Exception as e:
        return 'none'

    return query



def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    # Counts how many words are present in each predefined message
    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    # Calculates the percent of recognised words in a user message
    percentage = float(message_certainty) / float(len(recognised_words))

    # Checks that the required words are in the string
    # ager kisi sentance  mai koi required word hai toh usko bhi check karenge jiss dhundhne mai aasni ho
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    # Must either have the required words, or be a single response
    # dono mai se koi na koi hona cahiye nai to keywords mai clash ho sakta hai and that might give error
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0


def check_all_messages(message):
    highest_prob_list = {}

    # Simplifies response creation / adds it to the dict
    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list #local veriale jo ki ak scope tak he rahega 
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    # Responses ------------------------------------------------------------------------------------------------------

        #now here i am callig the function by their value and storing the bot_responce in the highest_prob_list
            #bot_respoce    #list_of_words#user_message                      #single_responce
    response('Hello!', ['hello', 'hi', 'hey', 'sup', 'heyo'], single_response=True)
    response('my name is EDITH', ['what', 'is', 'your', 'name'])
    response('See you!', ['bye', 'goodbye'], single_response=True)          #required_word
    response('I\'m doing fine, and you?', ['how', 'are', 'you', 'doing'], required_words=['how'])
    response('You\'re welcome!', ['thank', 'thanks'], single_response=True)
    response('Thank you!', ['i', 'love', 'code', 'katrina'], required_words=['code', 'katrina'])
    response('thats good', ['shivam', 'rishbh'])

    # Longer responses
    response(long.R_ADVICE, ['give', 'advice'], required_words=['advice'])
    response(long.R_EATING, ['what', 'you', 'eat'], required_words=['you', 'eat'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    #print(highest_prob_list)
    #print(f'Best match = {best_match} | Score: {highest_prob_list[best_match]}')

    return long.unknown() if highest_prob_list[best_match] < 1 else best_match


# Used to get the response
def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = check_all_messages(split_message)
    print(f"bot : {response}")
    return response


# Testing the response system
while True:
    query = takeCammand().lower()
    print(f"You :  {query}")
    speak(get_response(query))