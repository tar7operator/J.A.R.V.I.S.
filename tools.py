import math
import pyttsx3
import time
import webbrowser
import speech_recognition as sr
import csv
import wikipedia
import pyjokes

# definitions
engine = pyttsx3.init("sapi5")
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
r = sr.Recognizer()
m = sr.Microphone()
logfile = open('console.txt', "a", encoding='utf-8')


# set log to file
def setlog(log_data, logger):
    if len(log_data) < 60:
        logfile.write(time.ctime(time.time()) + " : " + logger + " : " + log_data + "\n")


# speaker
def speak(text):
    print(text)
    engine.say(text)
    engine.runAndWait()
    setlog(text, "JARVIS")


close_commands = {
    "close now": "Okay Sir.",
    "i don't want to talk right now": "Its Okay Sir, take a coffee to change your mood.",
    "you are stupid": "I am Sorry Sir, but i was made like this",
    "you are not good assistant": "Sorry for problem, will take this as feedback to improve myself"}

greet_commands = [
    "hello", "hi","dear", "jarvis", "friend"
]
gen_com = ["hello", "hi", "jarvis", "friends", "dear", "close", "stupid", "assistant", "good", "not", "mood", "good", "bad", "talk", "want", "don't", ]


# listener
def listen(x=""):
    with m as source:
        r.adjust_for_ambient_noise(source)
    print(x)
    with m as source:
        audio = r.listen(source)
    print("...")
    try:
        value = r.recognize_google(audio)
        print(value)
        setlog(value, "User")
        return value.lower()
    except sr.UnknownValueError:
        speak("Sorry! Can you tell me what you wanted to say?")
        return "None"
    except sr.RequestError:
        speak("Speech recognition is not working. Try again ..")
        return "None"


# websites--
def wiki(something):
    query = ""
    keys = ["who is", "in wikipedia", "tell me something about", "tell me about"]
    for i in keys:
        if i in something:
            query = something.replace(i, "")

    speak('Searching Wikipedia..')
    results = wikipedia.summary(query, sentences=2)
    speak("According to Wikipedia,")
    speak(results)


def youtube(something):
    query = "+".join(something.split())
    url = "https://www.youtube.com/results?search_query=" + query
    webbrowser.open(url)
    speak('Opening YouTube..')


def google(something):
    query = "+".join(something.split())
    url = "https://www.google.com/search?q=" + query
    webbrowser.open(url)
    speak('Opening Browser..')


# functions

def tell_time(value):
    current_time = time.localtime(time.time())

    hours = current_time.tm_hour
    minutes = current_time.tm_min
    days = current_time.tm_mday
    month = current_time.tm_mon
    year = current_time.tm_year
    month_names = {0: "January", 1: "February", 2: "March", 3: "April", 4: "May", 5: "June", 6: "July", 7: "August",
                   8: "September", 9: "October", 10: "November", 11: "December"}

    if hours > 12:
        meridian = "P.M."
        hours = hours - 12
    elif hours == 12:
        meridian = "P.M."
    else:
        meridian = "A.M."
    for mon in month_names:
        if mon + 1 == month:
            month = month_names[mon]

    if "date" in value:
        speak(str(days) + " " + month + " " + str(year))
    elif "time" in value or "clock" in value:
        speak("Current time is " + str(hours) + ":" + str(minutes) + " " + meridian)
    elif "year" in value:
        speak("Current year is " + str(year))
    elif "month" in value:
        speak("Current month is " + str(month))


def calculate():
    speak("Now in Calculate mode. Say 'exit' to return to normal")
    calculation = True

    while calculation:
        equation = listen("Tell the equation...")
        split = equation.split()
        answer = ""

        if "exit" in split:
            calculation = False
        elif "log" in split:
            logi = float(split[-1])
            if "base" in split:
                answer = math.log(logi, float(split[split.index("base") + 1]))
            else:
                answer = math.log(logi)
        elif "square root" in split or "root" in split:
            answer = math.sqrt(float(split[split.index("root") + 2]))
        elif "square" in split:
            answer = math.pow(float(split[split.index("square") + 2]), 2)
        elif "cube" in split:
            answer = math.pow(float(split[split.index("cube") + 2]), 3)
        elif "sine" in split:
            if "inverse" in split:
                answer = math.asin(float(split[split.index("inverse") + 2]))
            else:
                answer = math.sin(float(split[split.index("sine") + 2]))

        if calculation:
            speak(equation + " is " + str(answer))

    else:
        speak("Exiting mathematician mode.")


def set_remainder(something):
    if "reminder" in something:
        file = open("reminder.csv", "a", newline='')

        speak("What is the message to remind ?")
        r_message = listen("message of reminder...")
        speak("What should be the date to remind ?")
        r_date = listen("tell the date...")
        speak("What should be the time to remind ?")
        r_time = listen("tell the time...")

        fieldnames = ['time', 'date', 'message']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow({'message': r_message, 'time': r_time, 'date': r_date})

        speak("Reminder added successfully!")

    else:
        speak("I am sorry, i forgot what to do.")


def tell_joke(something):
    speak("Thinking of a joke..")
    joke = pyjokes.get_joke(language="en")
    speak(joke)
