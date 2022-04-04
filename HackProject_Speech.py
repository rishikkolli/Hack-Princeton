# Speech Recognition
from email.mime import audio
import speech_recognition
import pyttsx3

# Dates and Time Limit
import datetime

# Regular Expressions
import re


text_to_speech_converter = pyttsx3.init() # Text-to-Speech conversion
text_to_speech_rate = text_to_speech_converter.setProperty("rate", 150)
voices = text_to_speech_converter.getProperty("voices")
text_to_speech_converter.setProperty("voice", voices[1].id) # Set the voice to female

time_limit = datetime.datetime.now() + datetime.timedelta(minutes=1) # Have user speak for 1 minute
print("Starting Time: " + str(datetime.datetime.now()))

recognizer = speech_recognition.Recognizer() # Speech-to-Text conversion
text = "" # Stores user-spoken text
first_prompt = True

# Attribute variables
iteration = 1
is_sick = False
is_health_status_given = False
health_activities = list() # To store response to "How have you been keeping healthy?"
symptoms = list() # To store response to "What are your major symptoms?"


# Keywords Indicating User Health
healthy_pattern = ["i am healthy", "i'm healthy", "i am feeling healthy", "i'm feeling healthy", "i am good", "i'm good","i am feeling good", "i'm feeling good", "healthy", "felling healthy", "feeling good", "good"]

# Keywords Indicating User Illness
sick_pattern = ["i am sick", "i'm sick", "i am feeling sick", "i'm feeling sick", "i am bad", "i'm bad","i am feeling bad", "i'm feeling bad", "sick", "bad", "feeling sick", "feeling bad"]




####################################################################
def pattern_search(text, iteration):

    traversed_loop = False # To check if at least one of the loops was traversed

    if(iteration == 1):
        
        # Sick Check
        for x in range(0, len(sick_pattern)):
            
            if(re.search(sick_pattern[x], text) != None and x != len(sick_pattern) - 1):
                match = re.search(sick_pattern[x], text)
                matched_string = match.string

            elif(re.search(sick_pattern[x], text) == None and x == len(sick_pattern) - 1):
                #print("inside the sick break")
                break

            else:
                continue

            if(matched_string == sick_pattern[x]):
                is_sick = True
                is_health_status_given = True

                print("List your major symptoms (i.e., fever, sore throat, fatigue).")
                text_to_speech_converter.say("List your major symptoms (i.e., fever, sore throat, fatigue).")
                text_to_speech_converter.runAndWait()

                traversed_loop = True
                break # Exit the loop

        # Healthy Check
        if(traversed_loop == False):

            for y in range(0, len(healthy_pattern)):

                if(re.search(healthy_pattern[y], text) != None and y != len(healthy_pattern) - 1):
                    match = re.search(healthy_pattern[y], text)
                    matched_string = match.string

                elif(re.search(healthy_pattern[y], text) == None and y == len(healthy_pattern) - 1):
                    #print("inside the healthy break")
                    break

                else:
                    continue

                if(matched_string == healthy_pattern[y]):
                    is_sick = False
                    is_health_status_given = True

                    print("List your health habits (i.e., jogging, yoga, biking).")
                    text_to_speech_converter.say("List your health habits (i.e., jogging, yoga, biking).")
                    text_to_speech_converter.runAndWait()

                    break # Exit the loop
####################################################################




while True:
    
    if(datetime.datetime.now() >= time_limit):
        print("Ending Time: " + str(datetime.datetime.now()))
        break

    else:
        try:
                
            if(first_prompt):
                print("Hello, I am Aurora, your personal health care assistant, how are you feeling: healthy or sick today?")
                text_to_speech_converter.say("Hello, I am Aurora, your personal health care assistant, how are you feeling: healthy or sick today?")
                text_to_speech_converter.runAndWait()
                first_prompt = False

            with speech_recognition.Microphone() as mic:

                if(text == "" and iteration <= 2):
                    recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = recognizer.listen(mic)

                    text = recognizer.recognize_google(audio)
                    text = text.lower()

                elif(iteration > 2):
                    break

                print(f"Your Text: {text}")


                # Evaluate text and usher response
                pattern_search(text, iteration)


                # Write to file
                speech_file = open("speech_text.txt", "a")
                speech_file.write(text + "\n")

                text = "" # Reset
                iteration = iteration + 1

        except speech_recognition.UnknownValueError():
            recognizer = speech_recognition.Recognizer()

        except:
            print("END")

        finally:
            speech_file.close()
            is_sick = False
            is_health_status_given = False

from nltk import RegexpParser
from nltk import pos_tag
import nltk

with open("pythong\speech_text.txt", "r") as speech_text:
    lines = speech_text.readlines()

items = list()
for line in lines:
    items.append(line.replace("\n", ""))

word = list()

for item in items:
    eachItem = item.split()
    for i in eachItem:
        word.append(i)
#print("Items: " + str(items))
#print(word)

part_speech_list = pos_tag(word)
print(part_speech_list)

nouns = []
for word, pos in part_speech_list:
    if pos == 'NN':
        nouns.append(word)

adjectives = []
for word, pos in part_speech_list:
    if pos == 'JJ':
        adjectives.append(word)
print(nouns)

links = ["https://www.mayoclinic.org/diseases-conditions/fever/in-depth/fever/art-20050997", "https://www.medicalnewstoday.com/articles/322394", "https://www.mayoclinic.org/diseases-conditions/chronic-daily-headaches/in-depth/headaches/art-20047375", "https://www.mayoclinic.org/diseases-conditions/sore-throat/diagnosis-treatment/drc-20351640", "https://www.arthritis-health.com/blog/11-ways-relieve-pain-naturally", "https://www.healthline.com/health/diarrhea-and-vomiting", "https://www.healthline.com/health/home-treatments-for-shortness-of-breath"]
key_words = [["fever", "temperature", "illness"], ["cough", "fever", "infections", "allergies"], ["headaches", "head", "hurts"], ["sore throat", "fever", "muffled voice", "swallowing"], ["pain", "muscles", "sore", "soreness", "aches"], ["diarrhea", "vomiting" , "light", "light headed", "food poisoning"], ["shortness of breath", "asthma", "dyspnea"]]
        
for noun in nouns:
    for i in range(len(key_words)):
        for j in range(len(key_words[i])):
            if key_words[i][j] == noun:
                print(links[i])
