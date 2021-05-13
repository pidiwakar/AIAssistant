import webbrowser

import speech_recognition as sr
import pywhatkit as kit
import pyttsx3
import datetime
import pyjokes
import  os
import subprocess
import json
import  requests
import  wolframalpha

from wikipedia import wikipedia

listener = sr.Recognizer()
engine=pyttsx3.init()
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_cmd():
    try:
        with sr.Microphone() as source:
            print('listening....')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command=command.lower()
            if 'alexa' in command:
                command=command.replace('alexa','')
    except:
        pass
    return command
hour = int(datetime.datetime.now().hour)
minute = int(datetime.datetime.now().minute)

def run_alexa():
    command=take_cmd()
    print(command)
    if 'play' in command:
        song=take_cmd()
        print('playing'+song)
        talk('playing'+song)
        kit.playonyt(song)
    elif 'time' in command:
        talk('Now it is',hour,minute)
    elif 'wiki' in command:
        srch=take_cmd()
        info= wikipedia.summary(srch,3)
        print(info)
        talk('according to wikipedia'+info)
    elif 'joke' in command:
        talk(pyjokes.get_joke('english','funny'))
    elif 'message' in command:
        talk("please tell me the number on which I should send the message")
        n='+91'+input()
        talk("please tell me the message you wish to convey")
        msg = take_cmd()
        print(n)
        kit.sendwhatmsg(n, msg, hour,minute+2,10,True)
    elif 'news' in command:
        news=webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
        talk('here are some headlines from times of india')
    elif 'search' in command:
        talk('what would you like to search on web?')
        res=take_cmd()
        talk('okay,here are your results')
        kit.search(res)
    elif 'ask' in command:
        talk('I will try my best to answer your question, what do you want to know?')
        qstn = take_cmd()
        app_id="L8HWRQ-UWVQ3XL54K"
        client = wolframalpha.Client(app_id)
        res=client.query(qstn)
        ans=next(res.results).text
        talk(ans)
    elif 'direction' in command or 'map' in command:
        talk('Can you please tell me the starting location?')
        ini=take_cmd()
        talk('thanks, now can you please tell me where are you headed to?')
        des=take_cmd()
        webbrowser.open_new_tab("https://www,google.ca/maps/dir/" + ini+"/"+des)
    elif 'music' in command:
        talk('opening spotify...please wait')
        webbrowser.open_new_tab("https://open.spotify.com/")
    elif 'bye' in command or 'tata' in command or 'stop' in command:
        talk('Okay I am going now, have a nice day ahead')
        datetime.time.sleep(100)
    elif 'yourself' in command:
        talk('I am your personal assistant smarty, I can carry out your small tasks and help in saving your time and effort,I was made by piyush')
    elif 'weather' in command:
        api_key = "b675ff1bd4d0eed3a1392b61e1a0d712"
        base_url = "https://api.openweathermap.org/data/2.5/weather?"
        talk("what is the city name")
        city_name = take_cmd()
        complete_url = base_url + "&q=" + city_name + "&appid=" + api_key
        response = requests.get(complete_url)
        x = response.json()
        if x["cod"] != "404":
            y = x["main"]
            current_temperature = y["temp"] - 273
            current_temperature = round(current_temperature, 2)
            current_humidiy = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]
            talk(" Temperature is " +
                  str(current_temperature)+" degree celsius" +
                  "\n humidity in percentage is " +
                  str(current_humidiy) +
                  "\n description  " +
                  str(weather_description))
    elif 'log off' in command or 'shut down' in command:
        talk("Okay, your system will shut down in 10 seconds, make sure you closed all applications!")
        subprocess.call(["shutdown", "/1"])
    else:
        talk('please repeat what you said')
while True:
    run_alexa()