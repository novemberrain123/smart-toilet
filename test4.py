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

def takePic(folder, fileType):
    firebase2 = pyrebase.initialize_app(setConfig(1))
    auth2 = firebase2.auth()
    user2 = auth2.sign_in_with_email_and_password("bait2123.iot.03@gmail.com", "BeyondEducationH03")
    db2 = firebase2.database()
    storage2 = firebase2.storage()

    db2.child("PI_03_CONTROL").update({"camera": str(1)})
    print(str(datetime.now()))
    sleep(10)
    print(str(datetime.now()))
    db2.child("PI_03_CONTROL").update({"camera": str(0)})
    all_files = storage2.child("PI_03_CONTROL").list_files()
    for file in all_files:            
        try:
            if (file.name != "images/oled.jpg"):
                lastPic = file.name
        except:    
            print('File not found')   

    firebase2 = pyrebase.initialize_app(setConfig(0))
    auth2 = firebase2.auth()
    user2 = auth2.sign_in_with_email_and_password("bait2123.iot.03@gmail.com", "BeyondEducationH03")
    db2 = firebase2.database()
    storage2 = firebase2.storage()

    picPath = folder + "/" + fileType + "_" + strftime("%Y%m%d%H%M%S", localtime()) + ".jpg"
    storage2.child(lastPic).download("C:", "lastPic.jpg", user2['idToken'])
    storage1.child(picPath).put("C:/Users/lengz/smart-toilet/lastPic.jpg")

secondTime = 300
beginTime = 50

#display time actually spent pooing or urinating
peepooTime = str(int(secondTime - beginTime)) # To remove decimal points
lcdColor = {
    "lcdbkR": str(0),
    "lcdbkG": str(5),
    "lcdbkB": str(0),
}
db2.child("PI_03_CONTROL").update(lcdColor)
if (len(peepooTime) == 2): # Used 10 to 99 seconds
    db2.child("PI_03_CONTROL").update({"lcdtxt": "Time spent = " + peepooTime + "s"})
else: # Used 100 to 999 seconds
    db2.child("PI_03_CONTROL").update({"lcdtxt": "Time spent= " + peepooTime + "s"})
sleep(2)
takePic("lcdTime", "lt") # Take picture of time spent for pee or poo on lcd