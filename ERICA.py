import speech_recognition as sr
from pydub import AudioSegment 
from gtts import gTTS
import simpleaudio as sa
import pyglet
import os, sys
import time
import nltk
from nltk import word_tokenize
from nltk import Tree
import nltk.data
from stat_parser import Parser
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from nltk.tree import Tree
import re
import json


##Code to translate speech into text using the Google Cloud Speech API
##	Speak and print text (text to speech)
##  identify commands in text using natural language processing (not yet functional,
##		but most of the groundwork is laid. We can identify independent clauses, so we
##		cut out extra words like "Hey Erica" from the beginning. We can also identify
##		questions and differentiate them from statements)
##	Execute command
##  Allow the addition of new commands (sorta works in a roundabout way)

	
r = sr.Recognizer()

def speak(words):
	tts = gTTS(text=words, lang='en')
	filename = 'Erica.mp3'
	tts.save(filename)

	music = pyglet.media.load("Erica.mp3", streaming=False)
	print (words)
	music.play()

	time.sleep(music.duration) #prevent from killing
	os.remove(filename) #remove temperory file


with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    speak("Hi! I'm Erica. Ask me something")
    audio = r.listen(source)


print("Now processing audio input")

# recognize speech using Google Cloud Speech
GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""{
  "type": "service_account",
  "project_id": "[redacted]",
  "private_key_id": "[redacted]",
  "private_key": "-----BEGIN PRIVATE KEY-----\[redacted]\n-----END PRIVATE KEY-----\n",
  "client_email": "[redacted]",
  "client_id": "[redacted]",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://accounts.google.com/o/oauth2/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/[redacted]"
}
"""
def listen():
	try:
		return (r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS))
	except sr.UnknownValueError:
		return ("Google Cloud Speech could not understand audio")
	except sr.RequestError as e:
		return("Could not request results from Google Cloud Speech service; {0}".format(e))

test1 = listen()
print(test1)
text = word_tokenize(test1)
parser = Parser()
t = parser.parse(test1)
#parse_str = tostring(parsed, 'utf-8', method='xml')
#t = Tree.fromstring(parse_str)
print (t)
#string = str(parse_str)
#string.split('\n')
#stringjoined = string.splitlines()
#print (stringjoined)
#subtexts = []
#for subtree in t.subtrees():
#    if subtree.label()=="S" or subtree.label()=="SBAR":
        #print subtree.leaves()
#        subtexts.append(' '.join(subtree.leaves()))
#print subtexts

#question = False
#imperative = False
#statement = False

#presubtexts = subtexts[:]       # ADDED IN EDIT for leftover check

#for i in reversed(range(len(subtexts)-1)):
#    subtexts[i] = subtexts[i][0:subtexts[i].index(subtexts[i+1])]

#for text in subtexts:
#    print (text)

# ADDED IN EDIT - Not sure for generalized cases
#leftover = presubtexts[0][presubtexts[0].index(presubtexts[1])+len(presubtexts[1]):]
#print (leftover)

command = ""
ind = ""
vb = False
interrogative = False
statement = False
for subtree in t.subtrees():
	if "Q" in subtree.label():
		interrogative = True
	elif subtree.label()=="S" or subtree.label()=="SBAR":
		statment = True
	if "VB" in subtree.label():
		ind = subtree
		vb = True
if vb:
	index=str(ind)
	commands = index.split()
	command=commands[1]
	command = (command.replace(")", ""))




#functions for imperatives
def start(text):
	app = (text.index("start")) + 1
	os.system("sh open.sh \"" + text[app] +".app\"")
def weather(town):
	os.system("sh open.sh \"Terminal.app\"")
	os.system("sh weather.sh " + town)
	
# imperatives (We hope not to hardcode the cases in the future, but instead store the commands, the number of parameters expected, stored values, the executable file, and type of executable file the command is executed in in a JSON or similar format to read through here. If the command obtained by the natural language processing matches a command stored in the JSON file, we retrieve the executable and its type and execute it in python. We included the JSON file in our submission, but it does not yet work with the code)

if ((command == "start")or "start" in test1):
	start(text)
elif "weather" in test1:
	town = (text.index("weather")) + 2
	weather(text[town])
elif "elp me help you" in test1:
	speak("You can write a shell file and create a new function in ERICA.py. We hope to add the capability to store the commands in the cloud and to be able to add new commands remotely in the coming weeks")
	
#Questions  (e.g. what is my name? Who is the president?)

#Statments (e.g. My name is Joe. I have a dog, that can be stored locally for reference

## after ALL commands, then:
else:
	speak("I'm not sure how to do that, but you can tell me how. To find out more, say \"Help me help you\"")
