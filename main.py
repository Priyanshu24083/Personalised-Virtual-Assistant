import pyttsx3
import speech_recognition as sr
import datetime
import os
import webbrowser
import wikipedia
import pyjokes
import requests
import threading

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Converts text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Captures user speech input and returns it as text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language="en-in")
        print(f"User said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
        return None
    except sr.RequestError as e:
        print(f"Request error: {e}")
        return None

user_name = None

def greet_user():
    global user_name
    current_hour = datetime.datetime.now().hour
    if user_name is None:
        speak("What is your name?")
        user_name = listen()
    greeting = "Good morning" if current_hour < 12 else "Good afternoon" if current_hour < 18 else "Good evening"
    speak(f"{greeting}, {user_name} I am BILLY,How can I assist you today?")


def tell_time():
    """Tells the current time."""
    now = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"The current time is {now}")
    speak(f"The current time is {now}")

def tell_date():
    """Tells today's date."""
    today = datetime.datetime.today().strftime("%B %d, %Y")
    print(f"Today's date is {today}")
    speak(f"Today's date is {today}")

def tell_joke():
    """Tells a random joke."""
    joke = pyjokes.get_joke()
    print(joke)
    speak(joke)

def open_website(query):
    """Opens a website based on user input."""
    websites = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "attendance": "https://gu.icloudems.com/corecampus/index.php"
    }
    for key, url in websites.items():
        if key in query:
            speak(f"Opening {key}")
            webbrowser.open(url)
            return
    speak("Sorry, I can't open that website.")

def search_wikipedia(query):
    """Searches Wikipedia and reads a summary."""
    speak("Searching Wikipedia...")
    query = query.replace("search", "").replace("wikipedia", "").strip()
    try:
        result = wikipedia.summary(query, sentences=2)
        print(result)
        speak(result)
    except wikipedia.exceptions.DisambiguationError as e:
        speak("There are multiple results. Please be more specific.")
        print(f"Disambiguation error: {e.options}")
    except wikipedia.exceptions.PageError:
        speak("I couldn't find any relevant information.")
    except Exception as e:
        speak("An error occurred while searching Wikipedia.")
        print(f"Error: {e}")

def weather_update(city):
    """Provides the current weather for a specified city."""
    api_key = '73e1060b17449e4e85528d2216e1e5ab'
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("cod") != "404":
            temp = data["main"]["temp"]
            status = data["weather"][0]["description"]
            print(f"The temperature in {city} is {temp} degrees Celsius with {status}.")
            speak(f"The temperature in {city} is {temp} degrees Celsius with {status}.")
        else:
            speak(f"Couldn't find weather information for {city}.")
    except requests.RequestException as e:
        speak("Error fetching weather data.")

def open_application(query):
    apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "netflix": r"C:\Users\ASUS\Desktop\Netflix.lnk",
        "whatsapp": "C:\\Users\\ASUS\\Desktop\\WhatsApp.lnk"
    }
    for app, path in apps.items():
        if app in query:
            speak(f"Opening {app}.")
            os.system(path)
            return
    speak("Application not found.")

def system_control(query):
    if "shutdown" in query:
        speak("Shutting down the system.")
        os.system("shutdown /s /t 1")
    elif "restart" in query:
        speak("Restarting the system.")
        os.system("shutdown /r /t 1")
    elif "log off" in query:
        speak("Logging off the system.")
        os.system("shutdown /l")

def perform_calculation(expression):
    """Performs a simple arithmetic calculation."""
    try:
        result = eval(expression)
        print(f"The result is {result}")
        speak(f"The result is {result}")
    except Exception as e:
        print(f"Error: {e}")
        speak("I couldn't perform the calculation.")


def reset_chat():
    """Resets the assistant's session."""
    speak("Resetting your session. How can I assist you now?")
    print("Session reset! Ready for new instructions.")

def roommates(query):
    if "tushar" in query:
        print("Tushar is an atm that never runs out of balance and loves archie.")
        speak("Tushar is an atm that never runs out of balance and loves archie..")
    if "sudheer" in query:
        print("Sudheer is a heartbroken physics teacher.")
        speak("Sudheer is a heartbroken physics teacher.")
    if "kaushik" in query:
        print("Kaushik is a bookie that always wins alone but loses when i watch him.")
        speak("Kaushik is a bookie that always wins alone but loses when i watch him.")
    if "sanidhya" in query:
        print("Pub-G Lover Pub-G Lover Pub-G Lover Pub-G Lover Pub-G Lover Pub-G Lover.")
        speak("Pub-G Lover Pub-G Lover Pub-G Lover Pub-G Lover Pub-G Lover Pub-G Lover.")

def handle_query(query):
    """Handles user queries."""
    if "time" in query:
        tell_time()
    elif "date" in query:
        tell_date()
    elif "joke" in query:
        tell_joke()
    elif "open" in query:
        open_application(query)
    elif "show" in query:
        open_website(query)
    elif "wikipedia" in query:
        search_wikipedia(query)
    elif "shutdown" in query or "restart" in query or "log off" in query:
        system_control(query)
    elif "tushar" in query or "sudheer" in query or "kaushik" in query or "sanidhya" in query:
        roommates(query)
    elif "calculate" in query:
        expression = query.replace("calculate", "").strip()
        perform_calculation(expression)
    elif "weather" in query:
        speak("Which city?")
        city = listen()
        if city:
            weather_update(city)
    elif "reset chat" in query:
        reset_chat()
    elif "exit" in query or "quit" in query:
        speak("Goodbye! Have a nice day.")
        return False
    else:
        speak("Sorry, I didn't understand that.")
    return True

def run_virtual_assistant():
    """Runs the virtual assistant."""
    greet_user()
    while True:
        query = listen()
        if query:
            if not handle_query(query):
                break

if __name__ == "__main__":
    run_virtual_assistant()
