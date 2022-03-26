import re
import long_responses as long

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
    response('Hello there.', ['hello', 'hi', 'hey', 'sup', 'heyo','hii','hiii'], single_response=True)
    response('I am EDITH. Pleased to meet you ', ['what', 'is', 'your', 'name'], required_words='name')
    response('Now tell me your problem', ['i', 'am','fine', 'good'])
    response('See you!', ['bye', 'goodbye'], single_response=True)
    response('which type of problem you are getting', ['my', 'app' , 'is', 'not ', 'working', 'properly' ])
    response('Dr. Kapil chaturvedi', ['who','is','your','mentor'])
              #required_word
    response('I\'m doing fine, and you?', ['how', 'are', 'you', 'doing'], required_words=['how'])
    response('You\'re welcome!', ['thank', 'thanks'], single_response=True)
    response('Thank you!', ['i', 'love', 'code', 'katrina'], required_words=['code', 'katrina'])
    #response('thats good', ['shivam', 'rishabh'])
    # Longer responses 
    response(long.R_ADVICE, ['give', 'advice'], required_words=['advice'])
    response(long.R_EATING, ['what', 'you', 'eat'], required_words=['you', 'eat'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    print(highest_prob_list)
    print(f'Best match = {best_match} | Score: {highest_prob_list[best_match]}')
    return long.unknown() if highest_prob_list[best_match] < 1 else best_match


# Used to get the response
def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response


# Testing the response system


while True:
    print('Bot: ' + get_response(input('You: ')))