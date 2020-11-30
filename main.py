from time import *
from pyrebase import pyrebase
from datetime import *
import urllib.request, json
import random
import speech_recognition as sr
import pyttsx3
import pyaudio
from pathlib import Path
import math
from math import ceil
from PIL import Image
from PIL import ImageOps
from flask import Flask
app = Flask(__name__)

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

    storage2.child(lastPic).download("C:", "lastPic.jpg", user2['idToken'])
    if (folder == "wastage"):
        storage2.child(lastPic).download("C:", "wastage.jpg", user2['idToken']) #For detecting pee or poo type later

    picPath = folder + "/" + fileType + "_" + strftime("%Y%m%d%H%M%S", localtime()) + ".jpg"
    cwd = str(Path.cwd())
    cwd = '/'.join(cwd.split('\\'))
    storage1.child(picPath).put(cwd +"/lastPic.jpg")


def getLatestSubfolder():
    hour = str(datetime.now())[11:13]
    date = strftime("%Y%m%d", localtime())

    #Get the last child for the last sensor record which is Minute+Second, which is y

    y = db2.child("PI_03_" +
                  date).child(hour).order_by_key().limit_to_last(1).get()
    return y, hour, date


def updUltsensor(ultName):
    y, hour, date = getLatestSubfolder()
    for keyValue in y:
        x = str(keyValue.key())
        ultResults = db2.child("PI_03_" + date).child(hour).child(x).child(
            "rand1").get().val()  #record every 10 secs
        ultResults2 = db2.child("PI_03_" + date).child(hour).child(x).child(
            "rand2").get().val()  #record every 10 secs
        ultResults = min(ultResults, ultResults2)
        db1.child("main").child(day).child(count).update(
            {ultName: str(ultResults)})  #write ultrasensor results to db1
        return float(ultResults)


def updSensor(input, output):
    y, hour, date = getLatestSubfolder()
    for keyValue in y:
        x = str(keyValue.key())
        results = db2.child("PI_03_" + date).child(hour).child(x).child(input).get().val()
        db1.child("main").child(day).child(count).update({output: str(results)})


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
                print("Listening...")
                audio2 = r.listen(source2)
                print("Processing...")

                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()
                print(MyText)
                if MyText.split()[0] in (wash_v + flush_v) and len(MyText.split()) in [1,4]:
                    if (len(MyText.split()) == 1):
                        return MyText, True  #whether is default flush/wash time or not
                    elif not (MyText.split()[2].isdigit()):
                        print("Please repeat your command")
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
def findType(s):
    wastage = Image.open(s)

    rectangle = (130, 340, 200, 440)
    cropped_wastage = wastage.crop(rectangle)


    r1, g1, b1 = cropped_wastage_surrounding = cropped_wastage.getpixel((0,0))
    r2, g2, b2 = cropped_wastage_middle = cropped_wastage.getpixel((35,50))

    print(cropped_wastage_surrounding)
    print(cropped_wastage_middle)

    if (r1-r2) in range(-50,50) and (g1-g2) in range(-50,50) and (b1-b2) in range(-50,50): # pee
        if r1 in range(250,256) and g1 in range(250,256) and b1 in range(250,256): # clear pee
            wastageType = "pee_clear"
        else:
            wastageType = "pee_yellow"

    else: # poo
        if r2 in range(200,256) and g2 in range(200,256) and b2 in range(200,256): # black poo
            wastageType = "poo_black"
        else: 
            wastageType = "poo_yellow"
    return wastageType
#MAIN
day = strftime("%Y%m%d", localtime()) #subfolder initialization
count = "00"
c = 0
wash_v = ["wash", "war", "lasts", "watch"]  #list of words meant to mean wash
flush_v = ["flush", "flash", "lush", "slush", "flourish"]

while True:
    while str(datetime.now())[11:19]!="00:00:00":
        try:
            data = {
                "ultra1":"", #user distance to toilet
                "ultra2":"", #toilet bowl distance from one side to opposite side
                "time":"", #Actual time where defecating/urinating happened
                "sound":"", #Buzzer sound representing bidet washing
                "led":"", #Led light representing flushing
                "wastageType":"", #Type of wastage & its color
            }
            db1.child("main").child(day).child(count).update(data)
            #red light & white light == on, blue light & green light == off
            data = {
                "relay1": "1",
                "relay2": "1",
            }
            #if user detected turn relay1 and relay2 updUltsensor("ultra1")
            while True:
                if (1<= 20):
                    db2.child("PI_03_CONTROL").update(data)
                    break
                sleep(9)

            takePic("userIn", "ui") # Take pictures of relays on

            check = True
            while check: #updUltsensor("ultra2")
                if (1 <= 20):
                    beginTime = perf_counter()
                    while check:
                        if (333 > 20):
                            secondTime = perf_counter()
                            while check:
                                if (333 > 20):
                                    if ((perf_counter() - secondTime) > 15):
                                        check = False
                                else:
                                    break
            peepooTime = ceil(perf_counter() - beginTime - 15)
            #update time to main db
            db1.child("main").child(day).child(count).update({"time": str(peepooTime)})

            #random image is chosen and displayed
            cwd = str(Path.cwd())
            cwd = '/'.join(cwd.split('\\'))
            print(cwd)
            bin = [
                "pee_clear", "pee_yellow", "poo_black",
                "poo_yellow"
            ]
            x = random.choice(bin)
            print(x)
            randS = cwd + "/img/" + x + ".png"
            storage2.child("images/oled.jpg").put(randS)
            db2.child("PI_03_CONTROL").update({"oledsc": "1"})
            sleep(10)
            takePic("wastage", "wt") # wastage picture taken
            db2.child("PI_03_CONTROL").update({"oledsc": "0"})


            spokenCommand, isDefault = speechToText()

            #if wash is spoken, will wash (allowed multiple times), then flush
            while True: 
                if (spokenCommand.split(' ')[0] in wash_v):
                    washTime = int(
                        spokenCommand.split(' ')[2]) if not isDefault else 20
                    db2.child("PI_03_CONTROL").update({"buzzer": "1"})
                    timeout = (datetime.now() + timedelta(seconds=washTime)).time()  #loop time = washTime
                    timeout = datetime.combine(date.today(), timeout)
                    while True:
                        updSensor("sound", "sound")
                        if (datetime.now() > timeout):
                            break
                    db2.child("PI_03_CONTROL").update({"buzzer": "0"})
                    print("Done washing")
                    spokenCommand, isDefault = speechToText()
                else:
                    break
            
            #flushing
            flushTime = int(spokenCommand.split(' ')[2]) if not isDefault else 15
            db2.child("PI_03_CONTROL").update({"ledlgt": "1"})
            timeout = (datetime.now() + timedelta(seconds=flushTime)).time()
            timeout = datetime.combine(date.today(), timeout)
            while True:
                updSensor("light", "led")
                if (datetime.now() > timeout):
                    break
            db2.child("PI_03_CONTROL").update({"ledlgt": "0"})

            #display time actually spent pooing or urinating
            lcdColor = {
                "lcdbkR": str(0),
                "lcdbkG": str(5),
                "lcdbkB": str(0),
            }
            db2.child("PI_03_CONTROL").update(lcdColor)
            peepooTime = str(peepooTime)
            if (len(peepooTime) == 2): # Used 10 to 99 seconds
                db2.child("PI_03_CONTROL").update({"lcdtxt": "Time spent = " + peepooTime + "s"})
            elif(len(peepooTime)==1):
                db2.child("PI_03_CONTROL").update({"lcdtxt": "Time spent =  " + peepooTime + "s"})
            else: # Used 100 to 999 seconds
                db2.child("PI_03_CONTROL").update({"lcdtxt": "Time spent= " + peepooTime + "s"})
            sleep(2)
            takePic("lcdTime", "lt") # Take picture of time spent for pee or poo on lcd

            data = {
                "relay1": str(0),
                "relay2": str(0),
            }

            #detect user leaving & present report afterwards
            while True:
                if (updUltsensor("ultra1")>200):
                    db2.child("PI_03_CONTROL").update(data)
                    takePic("userOut", "uo") # Take pictures of relays off
                    break
            

            #TODO
            #detect poo/urine type based on pi image
            wastageType = findType("wastage.jpg")
            db1.child("main").child(day).child(count).update({"wastageType": wastageType})

            #give recommendations to user based on that
            #integrate python with javascript & deploy
            #data stored:
            #ultra1, ultra2, sound, light, time, wastagetype
            c += 1
            count = str(f'{c:02}')
            break
        except KeyboardInterrupt:
            exit
    day = strftime("%Y%m%d", localtime())