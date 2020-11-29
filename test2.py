from time import *
from pyrebase import pyrebase
from datetime import *
import urllib.request, json
import random
import speech_recognition as sr
import pyttsx3
import pyaudio
from pathlib import Path

def setConfig(x):
    if (x==0):
        config2 = {
            "apiKey": "AIzaSyAs_1NVtsjZ-LmTATAp0a0R5fK6XdKHaMU",
            "authDomain": "bait2123-202010-03.firebaseapp.com",
            "databaseURL": "https://bait2123-202010-03.firebaseio.com/",
            "storageBucket": "bait2123-202010-03.appspot.com"
        }
        return config2

    else:
        config2 = {
            "apiKey": "AIzaSyAs_1NVtsjZ-LmTATAp0a0R5fK6XdKHaMU",
            "authDomain": "bait2123-202010-03.firebaseapp.com",
            "databaseURL": "https://bait2123-202010-03.firebaseio.com/",
            "storageBucket": "bait2123-202010-03.appspot.com",
            "serviceAccount": ".vscode/bait2123-202010-03-firebase-adminsdk-xmqwi-1caf6b0286.json"
        }
        return config2


config1 = {
    "apiKey": "AIzaSyAH0JTJqYZaKiO-GssnbO9lIW_Z9-HMu0c",
    "authDomain": "smart-toilet-adc07.firebaseapp.com",
    "databaseURL": "https://smart-toilet-adc07.firebaseio.com/",
    "storageBucket": "smart-toilet-adc07.appspot.com"
}

firebase1 = pyrebase.initialize_app(config1)
auth1 = firebase1.auth()
user1 = auth1.sign_in_with_email_and_password("pleaseworkusob@gmail.com", "Aa123456")
db1 = firebase1.database()
storage1 = firebase1.storage()


firebase2 = pyrebase.initialize_app(setConfig(0))
auth2 = firebase2.auth()
user2 = auth2.sign_in_with_email_and_password("bait2123.iot.03@gmail.com", "BeyondEducationH03")
db2 = firebase2.database()
storage2 = firebase2.storage()

c = 0  #subfolder initialization

wash_v = ["wash", "war", "lasts", "watch"]  #list of words meant to mean wash
flush_v = ["flush", "flash", "lush", "slush", "flourish"]


def speechToText():

    timeout = (datetime.now() + timedelta(seconds=60)).time()
    timeout = datetime.combine(date.today(), timeout)
    #if user doesnt give a correct command in 60s, toilet will flush automatically
    while True:
        try:
            with sr.Microphone() as source2:

                r = sr.Recognizer()
                r.adjust_for_ambient_noise(source2, duration=0.2)

                #listens for the user's input
                print("Listening.....")
                audio2 = r.listen(source2)
                print("Processing.....")

                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()
                print(MyText)
                if MyText.split()[0] in (wash_v + flush_v) and len(MyText.split()) in [1,4]:
                    if (len(MyText.split()) == 1):
                        return MyText, True  #whether is default flush/wash time or not
                    else:
                        return MyText, False
                else:
                    print("Please repeat your command")

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("Please repeat")

        finally:
            if (datetime.now() > timeout):
                return "flush", True

speechToText()
