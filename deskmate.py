import datetime
import os
import sys
import requests
import webbrowser
import cv2
import wolframalpha
from pynput.keyboard import Key,Controller
from time import sleep
import pyautogui 
import pyttsx3
import wikipedia
import pywhatkit as kit
import speech_recognition as sr
import keyboard
from newsapi import NewsApiClient


engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
def default_response():
    """
    This function provides a default response when the assistant doesn't recognize the user's command.
    """
    response = "I didn't understand that. Can you please repeat?"
    print(response)
    speak(response)
# Text to speech
def speak(audio):
    engine.say(audio)
    engine.runAndWait()


# Function to fetch news articles using the News API
def takecommand_news():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for news command....")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            print("No command heard. Continuing to the next news.")
            return "yes"  # Continue fetching the next news
    try:
        print("Recognizing news command...")
        query = r.recognize_google(audio, language='en-in')
        query = query.lower()
        print(f"User said: {query}")
        return query
    except Exception as e:
        print("Could not understand the news command. Continuing to the next news.")
        return "yes"  # Continue fetching the next news

# Modify the fetch_news function to use the new takecommand_news function
def fetch_news():
    newsapi = NewsApiClient(api_key='922c7007bdd845809c0f61e57067b47c')
    top_headlines = newsapi.get_top_headlines(country='in')  # 'in' is the country code for India

    articles = top_headlines['articles']

    for index, article in enumerate(articles, start=1):
        title = article['title']
        description = article['description']
        print(f"Headline {index}: {title}")
        print(f"Description: {description}\n")

        speak(f"Headline {index}: {title}")
        speak(f"Description {index}: {description}")

        # After reading one news, ask the user if they want to continue
        speak("Do you want to continue for the next news?")
        response = takecommand_news()
        if "no" in response:
            break


# Function to open Notepad
def open_notepad():
    npath = "C:\\Windows\\System32\\notepad.exe"
    os.startfile(npath)

# Function to open Visual Studio Code
def open_vscode():
    vpath = r"C:\Users\srees\AppData\Local\Programs\Microsoft VS Code\Code.exe"
    os.startfile(vpath)

# Function to get time
def get_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    return current_time


# Function to open YouTube
def search_youtube(query):
    speak("Sir, what should I search ?")
    cm = takecommand().lower()
    webbrowser.open(f"https://www.youtube.com/search?q={cm}")

# Function to increase volume
def volumeup():
    for i in range(5): 
        keyboard.press_and_release("volume up")

# Function to decrease volume
def volumedown():
    for i in range(5): 
        keyboard.press_and_release("volume down")

# Function to open facebook   
def open_facebook():
    webbrowser.open("https://www.facebook.com")


# Function to search on Google
def search_google(query):
    speak("Sir, what should I search on Google?")
    cm = takecommand().lower()
    webbrowser.open(f"https://www.google.com/search?q={cm}")

# Function to provide information about the assistant
def get_assistant_info():
    speak("I am Your DeskMate")

# Function to search
def perform_search(query):
    search_query = query.strip()
    webbrowser.open(f"https://www.google.com/search?q={search_query}")

# Function to take screenshot
def get_screenshot():
    num_screenshots = 1
    for i in range(num_screenshots):
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"ss_{timestamp}_{i}.jpg"
        im = pyautogui.screenshot()
        im.save(filename)
    speak(f"{num_screenshots} screenshots taken.")

# Function to exit the assistant
def exit_assistant():
    speak("Thanks for using me sir. Have a good day.")
    sys.exit()

# Function to handle the logic for tasks
def handle_tasks(query):
    if "open notepad" in query:
        open_notepad()
    elif "open vs code" in query:
        open_vscode()
    elif "screenshot" in query:
        get_screenshot()
    elif  "youtube" in query:
        search_youtube(query)
    elif "open" in query and "facebook" in query:
        open_facebook()
    elif "time" in query:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        response = f"The current time is {current_time}"
        print(response)
        speak(response)
    elif "volume up" in query:
        volumeup()
    elif "volume down" in query:
        volumedown()
    elif "search" in query:
        perform_search(query)
    elif "open" in query and "google"in query or "chrome" in query:
        search_google(query)
    elif "who are you" in query:
        get_assistant_info()
    elif "no thanks" in query or "thank you" in query or "good" and "bye" in query:
        exit_assistant()
    elif "news" in query:
        fetch_news()
    else:
        speak("Can you say that again?")


# Convert voice into text
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            speak("Sorry, I didn't hear any input. Please try again.")
            return "none"
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        query = query.lower()  # Convert query to lowercase
        print(f"User said: {query}")
    except Exception as e:
        speak("Sorry, I couldn't understand.")
        return "none"
    return query


# To wish the user
def wish():
    current_time = get_time()
    hour = datetime.datetime.now().hour

    if hour >= 0 and hour < 12:
        speak(f"Good morning!")
    elif hour >= 12 and hour < 18:
        speak(f"Good afternoon!")
    elif hour >= 18 and hour < 22:
        speak(f"Good evening!")
    else:
        speak(f"Good night!")

    speak("I am Your DeskMate. Please tell me how can I help you.")


if __name__ == "__main__":
    wish()
    while True:
        query = takecommand().lower()
        handle_tasks(query) 