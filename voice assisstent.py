import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import datetime
import os
import requests

# Initialize the recognizer and the text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen for audio input and return text
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
        except sr.RequestError:
            speak("Sorry, my speech service is down.")
        return ""

# Function to get the current time
def get_time():
    now = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {now}")

# Function to get the current date
def get_date():
    today = datetime.datetime.today().strftime("%B %d, %Y")
    speak(f"Today's date is {today}")

# Function to get weather information
def get_weather(city):
    api_key = "your_openweathermap_api_key"  # Replace with your OpenWeatherMap API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
    response = requests.get(complete_url)
    data = response.json()
    if data["cod"] != "404":
        main = data["main"]
        temperature = main["temp"]
        weather_desc = data["weather"][0]["description"]
        speak(f"The temperature in {city} is {temperature} degrees Celsius with {weather_desc}")
    else:
        speak("City not found")

# Main function to process commands
def process_command(command):
    if 'time' in command:
        get_time()
    elif 'date' in command:
        get_date()
    elif 'weather' in command:
        speak("Which city?")
        city = listen()
        if city:
            get_weather(city)
    elif 'wikipedia' in command:
        speak("What do you want to know about?")
        query = listen()
        if query:
            summary = wikipedia.summary(query, sentences=2)
            speak(summary)
    elif 'open' in command and 'browser' in command:
        speak("What do you want to search for?")
        query = listen()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            speak(f"Here are the results for {query}")
    elif 'open command prompt' in command or 'open cmd' in command:
        os.system("start cmd")
    elif 'greet' in command:
        speak("Hello, how can I assist you today?")
    else:
        speak("Sorry, I did not understand that command.")

# Main loop
if __name__ == "__main__":
    speak("How can I help you today?")
    while True:
        command = listen()
        if command:
            process_command(command)
