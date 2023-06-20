import festival
import time
import speech_recognition as sr
import os
import datetime
import openai

openai.api_key = "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"
ALERT="sunlight"

def listen4Alert():
    while True:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio_data = r.record(source, duration=4)
            try:
                text = r.recognize_google(audio_data)
            except:
                text = ""
            del(r)
            if text.find(ALERT)!=-1:
                print("found alert, processing request")
                return True

def parseQUERY():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio_data = r.record(source, duration=5)
        print("Recognizing...")
        try:
            text = r.recognize_google(audio_data)
        except:
            text = ""
        print(text)
        del(r)
        return text

def timeCMD(txt):
    now = datetime.datetime.now()
    return "The current time is " + str(now.hour) + " hours and " + str(now.minute) + " minutes"

festival.sayText('Hello and welcome to the Sunlight virtual assistant. Say hello sunlight to catch my attention')
print("listening...")
while True:
    if listen4Alert()==True:
        festival.sayText('hello, how can I help you?')
        v = parseQUERY()
        response = openai.Completion.create(model="text-davinci-003", prompt=v, temperature=0.5, max_tokens=100,top_p=1,frequency_penalty=0.2,presence_penalty=0,stop=["\"\"\""])
        answer = response["choices"][0]["text"]
        print("ANSWER: " + answer)
        festival.sayText(answer)
        print("listening...")
    if v == "exit":
        break;

