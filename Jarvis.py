import time
from tools import listen, speak, wiki, google, youtube, close_commands, tell_time, calculate, set_remainder, tell_joke


# working functions

def check_wiki(something):
    keys = ["who is", "in wikipedia", "tell me something about", "tell me about"]
    for w in keys:
        if w in something:
            return True
    else:
        return False


def has_joke(something):
    joke_keys = ["joke", "tell", "random", "make", "laugh", "want", "laugh", "right now", ]
    algo = 0
    for key in joke_keys:
        if key in something:
            algo += 1

    if algo >= 3:
        return True
    elif ("laugh" in something or "joke" in something) and algo >= 2:
        return True
    else:
        return False


def play():
    print("you ordered to play something")


def open_app(something):
    app_keys = ["open", "run", "initiate", "app", ""]
    apps = [{"notepad": "notepad"}]


def browse(something):
    if "youtube" in something:
        query = something.replace("search", "")
        query = query.replace("in youtube", "")
        youtube(query)
    elif "search" in something and "in google" in something:
        query = something.replace("search", "")
        query = query.replace("in google", "")
        google(query)
    elif "search" in something:
        query = something.replace("search", "")
        google(query)


def check_time(something):
    keys = ["date", "time", "what", "tell", "right", "current", "now", "position", "clock", "point", "year", "month",
            "going", "going on"]
    default = ["date", "time", "clock", "year", "month"]
    algo = 0
    has_time = False
    for key in keys:
        if key in something:
            algo += 1
    for key_2 in default:
        if key_2 in something:
            has_time = True

    if has_time and algo >= 2:
        return True
    elif "time" and algo >= 3:
        return True
    elif "time" == something or "date" == something or "month" == something or "year" == something:
        return True
    else:
        return False


def check_reminder(something):
    reminder_keys = ["set", "add", "update", "reminder", "message", "time", "change"]
    default = ["message", "time", "reminder"]
    algo = 0
    has_com = False

    for key in reminder_keys:
        if key in something:
            algo += 1
    for key_2 in default:
        if key_2 in something and "reminder":
            has_com = True

    if algo >= 2 and has_com:
        return True
    else:
        return False


Again = True

while Again:
    value = listen("Listening...")
    value_split = value.split()

    if value in close_commands:
        for i in close_commands:
            if value in i:
                speak(close_commands[i])
                Again = False
    elif value == "None":
        continue
    else:
        if value_split[0] == "play":
            play()
        elif value_split[0] == "open":
            open_app(value)
        elif value_split[0] == "calculate":
            calculate()
        elif check_wiki(value):
            wiki(value)
        elif check_time(value):
            tell_time(value)
        elif check_reminder(value):
            set_remainder(value)
        elif has_joke(value):
            tell_joke(value)
        else:
            browse(value)
    time.sleep(2)

else:
    speak("I am now closing myself.")
