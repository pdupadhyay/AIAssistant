import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser as wb
import requests, json
import pyjokes
import os
import pyautogui
import wolframalpha
import random
from dotenv import load_dotenv

engine = pyttsx3.init()
load_dotenv()
wolframalpha_api_id = os.getenv("wolframalpha_api_id")
openweatherapi_id = os.getenv("openweatherapi_id")

def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def time_():
    time = datetime.datetime.now().strftime("%H:%M:%S")
    speak("The current time is")
    speak(time)


def date_():
    date = datetime.datetime.now().date()
    speak("Today's date is")
    speak(date)


def wishme():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning PD")
    elif 12 <= hour < 18:
        speak("Good afternoon PD")
    elif 18 <= hour < 24:
        speak("Good evening PD")
    else:
        speak("Good night PD")
    speak("Welcome back")


def weather():
    speak("What's the name of the place?")
    city = take_command().lower()
    response = requests.get("http://api.openweathermap.org/data/2.5/weather?appid=" +openweatherapi_id+ "&q="+city)
    weather_json = response.json()
    if weather_json['cod'] != '404':
        current_weather = weather_json['main']
        current_temperature = current_weather['temp']
        current_pressure = current_weather['pressure']
        current_humidity = current_weather['humidity']
        description = weather_json['weather'][0]['description']
        print(" Temperature = " + str(current_temperature) +
          "\n Atmospheric pressure = " + str(current_pressure) +
          "\n Humidity = " + str(current_humidity) +
          "\n Description = " + str(description))
        speak("Currently in" + city + ", it's" + str(current_temperature) + "kelvin, with" + description)
    else:
        speak("I cannot find that place, please try again")
        return None


def joke():
    joke = pyjokes.get_joke()
    print(joke)
    speak(joke)


def write_note():
    speak("What should I write?")
    notes = take_command()
    file = open('C:/Users/samee/Desktop/notes.txt', 'w')
    file.write(notes)
    speak("Done taking notes.")


def show_notes():
    speak("Showing notes")
    file = open('C:/Users/samee/Desktop/notes.txt', 'r')
    notes = file.read()
    print(notes)
    speak(notes)


def screenshot():
    img = pyautogui.screenshot()
    img.save('C:/Users/samee/OneDrive/Pictures/Screenshots/screenshot.png')


def close():
    speak("Bye PD, have a nice day")


def take_command():
    command = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        command.pause_threshold = 1
        current_command = command.listen(source)

    try:
        print("Recognizing")
        query = command.recognize_google(current_command)
        print(query)

    except Exception as e:
        print(e)
        speak("I was not able to catch that, please try again")
        return take_command()
    return query


if __name__ == '__main__':
    wishme()
    functions = ["Tell current weather", "Tell you a joke", "Make and show notes", "Take Screenshot",
                 "Remember anything you say", "Perform Mathematical Calculations", "Locate a place",
                 "Search anything on YouTube and Google"]
    print("Speak these words to make me do a task:\n"
          "Date: To know today's date\n"
          "Time: To know current time\n"
          "Weather: To know about current weather of any city\n"
          "Tell me a joke: To make Chota Don tell a joke\n"
          "Write a note: To make a note\n"
          "Show notes: To show the notes\n"
          "Take Screenshot: To take the screenshot\n"
          "Remember that: To make Chota don remember something\n"
          "Do you remember?: Know what Chota don remembers\n"
          "Calculate: To perform mathematical calcuations\n"
          "Where is {place}: To search for a place on Google Maps\n"
          "Play on Youtube: To play videos on YouTube\n"
          "Bye/Close: To close the application")

    while True:
        query = take_command().lower()
        try:
            if 'time' in query:
                time_()

            elif 'date' in query:
                date_()

            elif 'thank you' in query:
                speak("Your Welcome")

            elif 'what is your name' in query:
                speak("My name is Chota Don.")

            elif 'what is my name' in query:
                speak("Your name is PD.")

            elif 'weather' in query:
                weather()

            elif 'joke' in query:
                joke()

            elif 'write a note' in query:
                write_note()

            elif 'show note' in query:
                show_notes()

            elif 'take screenshot' in query:
                screenshot()

            elif 'remember that' in query:
                speak('What should I remember?')
                memory = take_command()
                speak("Do you want me to remember "+memory + "?")
                reply = take_command().lower()
                if 'yes' in reply or 'yeah' in reply or 'sure' in reply:
                    remember = open('memory.txt', 'w')
                    remember.write(memory)
                    remember.close()
                else:
                    speak("I'm not remembering "+memory)

            elif 'do you remember' in query:
                remember = open('memory.txt', 'r')
                speak("You asked me to remember that "+remember.read())

            elif 'what is' in query or 'who is' in query:
                speak("Searching")
                client = wolframalpha.Client(wolframalpha_api_id)
                result = client.query(query)
                try:
                    print(next(result.results).text)
                    speak(next(result.results).text)
                except StopIteration:
                    print("No Result")
                    speak("Sorry, I can't find that")

            elif 'calculate' in query:
                speak("Calculating")
                client = wolframalpha.Client(wolframalpha_api_id)
                query = query.replace("calculate", "")
                answer = client.query(query)
                print("The answer is: "+next(answer.results).text)
                speak("The answer is: "+next(answer.results).text)

            elif 'where is' in query:
                query = query.replace("where is", "")
                speak("Locating "+query)
                wb.open("https://www.google.com/maps/place/"+query)

            elif 'youtube' in query:
                speak("Opening Youtube")
                query = query.replace('on youtube', '')
                wb.open("https://www.youtube.com/search?q="+query)

            elif 'what can you do' in query:
                speak(random.sample(functions, 4))

            #elif 'open' in query:
            #    application = query.replace('open', '')
            #    speak("Opening"+application)
            #    os.system("start " + application + ".exe")

            elif 'bye' in query or 'close' in query:
                close()
                break

            else:
                speak("Searching on Google")
                wb.open("https://www.google.com/search?q="+query)

        except Exception as e:
            print(e)
            speak("I was not able to catch that, try again")
