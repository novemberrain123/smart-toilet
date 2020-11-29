from time import *
from pyrebase import pyrebase
from datetime import *
import urllib.request, json
import random
import speech_recognition as sr
import pyttsx3
import pyaudio
from pathlib import Path
from PIL import Image
from PIL import ImageOps

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

wastage = Image.open("wastage.jpg")

rectangle = (130, 340, 200, 440)
cropped_wastage = wastage.crop(rectangle)

cropped_wastage.show()

r1, g1, b1 = cropped_wastage_surrounding = cropped_wastage.getpixel((0,0))
r2, g2, b2 = cropped_wastage_middle = cropped_wastage.getpixel((35,50))

print(cropped_wastage_surrounding)
print(cropped_wastage_middle)

if (r1-r2) in range(-5,6) and (g1-g2) in range(-5,6) and (b1-b2) in range(-5,6): # pee
    if r1 in range(250,256) and g1 in range(250,256) and b1 in range(250,256): # clear pee
        wastageType = "pee_clear"
    elif r1 in range(0,6) and g1 in range(0,6) and b1 in range(0,6): # yellow pee
        wastageType = "pee_yellow"
    else: # pink pee
        wastageType = "pee_pink"
else: # poo
    if r2 in range(250,256) and g2 in range(250,256) and b2 in range(250,256): # black poo
        wastageType = "poo_black"
    elif r2 in range(0,6) and g2 in range(0,6) and b2 in range(0,6): # yellow poo
        wastageType = "poo_yellow"
    else: # pink poo
        wastageType = "poo_brown"

print(wastageType)