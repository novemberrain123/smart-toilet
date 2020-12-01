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
from flask import Flask, render_template, Response
from flask.helpers import url_for
import numpy as np
from threading import Thread
app = Flask(__name__)
#MAIN
day = strftime("%Y%m%d", localtime())  #subfolder initialization
count = "00"
c = 0
wash_v = ["wash", "war", "lasts", "watch"]  #list of words meant to mean wash
flush_v = ["flush", "flash", "lush", "slush", "flourish"]
stop_run = False


def setConfig(x):
    if (x == 0):
        config2 = {
            "apiKey": "AIzaSyAs_1NVtsjZ-LmTATAp0a0R5fK6XdKHaMU",
            "authDomain": "bait2123-202010-03.firebaseapp.com",
            "databaseURL": "https://bait2123-202010-03.firebaseio.com/",
            "storageBucket": "bait2123-202010-03.appspot.com"
        }
        return config2

    else:
        config2 = {
            "apiKey":
            "AIzaSyAs_1NVtsjZ-LmTATAp0a0R5fK6XdKHaMU",
            "authDomain":
            "bait2123-202010-03.firebaseapp.com",
            "databaseURL":
            "https://bait2123-202010-03.firebaseio.com/",
            "storageBucket":
            "bait2123-202010-03.appspot.com",
            "serviceAccount":
            ".vscode/bait2123-202010-03-firebase-adminsdk-xmqwi-1caf6b0286.json"
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
user1 = auth1.sign_in_with_email_and_password("pleaseworkusob@gmail.com",
                                              "Aa123456")
db1 = firebase1.database()
storage1 = firebase1.storage()

firebase2 = pyrebase.initialize_app(setConfig(0))
auth2 = firebase2.auth()
user2 = auth2.sign_in_with_email_and_password("bait2123.iot.03@gmail.com",
                                              "BeyondEducationH03")
db2 = firebase2.database()
storage2 = firebase2.storage()


def generateReport(day):
    y = db1.child("main").child(day).order_by_key().get()
    for keyValue in y:
        x = str(keyValue.key())
        timeList = []
        typeList = []
        temp = float(
            db1.child("main").child(day).child(x).child("time").get().val())
        timeList.append(temp)
        temp = db1.child("main").child(day).child(x).child(
                "wastageType").get().val()
        typeList.append(temp)
    normalPeePooTime = 60
    normalPeeCount = 7
    normalPooCount = 1
    averagePeePooTime = np.mean(timeList)
    peeCount = 0
    pooCount = 0
    totalScore = 0
    totalScore += (normalPeePooTime / averagePeePooTime) * 0.1
    for wType in typeList:
        if (wType[:3] == "pee"):
            peeCount += 1
            if (wType == "pee_clear"):
                totalScore += 1.2 * 0.2
            else:
                totalScore += 1 * 0.2
        else:
            pooCount += 1
            if (wType == "poo_yellow"):
                totalScore += 1.2 * 0.2
            else:
                totalScore += 1 * 0.2
    totalScore += (peeCount / normalPeeCount) * 0.25 + (pooCount /
                                                        normalPooCount) * 0.25
    totalScore /= 3 + len(typeList)
    peepoo = {
        "averagePeePooTime": averagePeePooTime,
        "peeCount": peeCount,
        "pooCount": pooCount,
    }
    db1.child("main").child(day).update(peepoo)


def takePic(folder, fileType):
    firebase2 = pyrebase.initialize_app(setConfig(1))
    auth2 = firebase2.auth()
    user2 = auth2.sign_in_with_email_and_password("bait2123.iot.03@gmail.com",
                                                  "BeyondEducationH03")
    db2 = firebase2.database()
    storage2 = firebase2.storage()

    db2.child("PI_03_CONTROL").update({"camera": str(1)})
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
    user2 = auth2.sign_in_with_email_and_password("bait2123.iot.03@gmail.com",
                                                  "BeyondEducationH03")
    db2 = firebase2.database()
    storage2 = firebase2.storage()

    storage2.child(lastPic).download("C:", "lastPic.jpg", user2['idToken'])
    if (folder == "wastage"):
        storage2.child(lastPic).download(
            "C:", "wastage.jpg",
            user2['idToken'])  #For detecting pee or poo type later

    picPath = folder + "/" + fileType + "_" + strftime("%Y%m%d%H%M%S",
                                                       localtime()) + ".jpg"
    cwd = str(Path.cwd())
    cwd = '/'.join(cwd.split('\\'))
    storage1.child(picPath).put(cwd + "/lastPic.jpg")


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
        ult1 = db2.child("PI_03_" + date).child(hour).child(x).child(
            "rand1").get().val()  #record every 10 secs
        ult2 = db2.child("PI_03_" + date).child(hour).child(x).child(
            "rand2").get().val()  #record every 10 secs
        ultResults = min(int(float(ult1)), int(float(ult2)))
        db1.child("main").child(day).child(count).update(
            {ultName: str(ultResults)})  #write ultrasensor results to db1
        return float(ultResults)


def updSensor(input, output):
    y, hour, date = getLatestSubfolder()
    for keyValue in y:
        x = str(keyValue.key())
        results = db2.child("PI_03_" + date).child(hour).child(x).child(
            input).get().val()
        db1.child("main").child(day).child(count).update(
            {output: str(results)})


def speechToText():

    timeout = (datetime.now() + timedelta(seconds=60)).time()
    timeout = datetime.combine(date.today(), timeout)
    #if user doesnt give a correct command in 60s, toilet will flush automatically
    while True:
        try:
            with sr.Microphone() as source2:

                r = sr.Recognizer()
                r.adjust_for_ambient_noise(source2, duration=1)

                #listens for the user's input
                outputConsole("Listening...")
                sleep(1)
                audio2 = r.listen(source2)
                outputConsole("Processing...")

                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()
                outputConsole("You said: {}".format(MyText))
                if MyText.split()[0] in (wash_v + flush_v) and len(
                        MyText.split()) in [1, 4]:
                    if (len(MyText.split()) == 1):
                        return MyText, True  #whether is default flush/wash time or not
                    elif not (MyText.split()[2].isdigit()):
                        outputConsole("Repeat your command...")
                    else:
                        return MyText, False
                else:
                    outputConsole("Repeat your command...")

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            outputConsole("Repeat your command...")

        finally:
            if (datetime.now() > timeout):
                return "flush", True


def findType(s):
    wastage = Image.open(s)

    rectangle = (130, 340, 200, 440)
    cropped_wastage = wastage.crop(rectangle)

    r1, g1, b1 = cropped_wastage_surrounding = cropped_wastage.getpixel((0, 0))
    r2, g2, b2 = cropped_wastage_middle = cropped_wastage.getpixel((35, 50))

    print(cropped_wastage_surrounding)
    print(cropped_wastage_middle)

    if (r1 - r2) in range(-50, 50) and (g1 - g2) in range(
            -50, 50) and (b1 - b2) in range(-50, 50):  # pee
        if r1 in range(250, 256) and g1 in range(250, 256) and b1 in range(
                250, 256):  # clear pee
            wastageType = "pee_clear"
        else:
            wastageType = "pee_yellow"

    else:  # poo
        if r2 in range(200, 256) and g2 in range(200, 256) and b2 in range(
                200, 256):  # black poo
            wastageType = "poo_black"
        else:
            wastageType = "poo_yellow"
    return wastageType


def outputConsole(s):
    print(s)
    db1.child("main").update({"console": s})


@app.route('/')
def index():
    return render_template('index.html')


def run():
    global stop_run
    while not stop_run:
        sleep(1)
        try:
            global count
            day = strftime("%Y%m%d", localtime())
            outputConsole("Started...")
            data = {
                "ultra1": "",  #user distance to toilet
                "ultra2": "",  #distance between toilet bowl sides
                "time": "",  #Actual time where waste happened
                "sound": "",  #Buzzer sound representing bidet washing
                "led": "",  #Led light representing flushing
                "wastageType": "",  #Type of wastage & its color
            }
            db1.child("main").child(day).child(count).update(data)
            #red light & white light == on, blue light & green light == off
            data = {
                "relay1": "1",
                "relay2": "1",
            }
            #if user detected turn relay1 and relay2 updUltsensor("ultra1")
            while True:
                if (1 <= 100):
                    db2.child("PI_03_CONTROL").update(data)
                    break
                sleep(9)

            takePic("userIn", "ui")  # Take pictures of relays on
            outputConsole("User has entered...")

            #record time user spends on toilet actually pooing/peeing
            #if ultra2 is >20 for more than 15 secs, considered to be done & timer will stop
            check = True
            while check:  #updUltsensor("ultra2")
                if (1 <= 10):
                    beginTime = perf_counter()
                    while check:
                        if (22 > 10):
                            secondTime = perf_counter()
                            while check:
                                if (22 > 10):
                                    if ((perf_counter() - secondTime) > 15):
                                        check = False
                                else:
                                    break
                                sleep(9)
                        sleep(9)
                sleep(9)

            peepooTime = ceil(perf_counter() - beginTime - 15)
            #update time to main db
            db1.child("main").child(day).child(count).update(
                {"time": str(peepooTime)})
            outputConsole("User has finished...")

            #random image is chosen and displayed
            cwd = str(Path.cwd())
            cwd = '/'.join(cwd.split('\\'))
            bin = ["pee_clear", "pee_yellow", "poo_black", "poo_yellow"]
            x = random.choice(bin)
            print(x)
            randS = cwd + "/img/" + x + ".png"
            storage2.child("images/oled.jpg").put(randS)
            db2.child("PI_03_CONTROL").update({"oledsc": "1"})
            sleep(10)
            takePic("wastage", "wt")  # wastage picture taken
            db2.child("PI_03_CONTROL").update({"oledsc": "0"})
            outputConsole("Image of wastage taken...")

            spokenCommand, isDefault = speechToText()

            #if wash is spoken, will wash (allowed multiple times), then flush
            while True:
                if (spokenCommand.split(' ')[0] in wash_v):
                    washTime = int(
                        spokenCommand.split(' ')[2]) if not isDefault else 20
                    db2.child("PI_03_CONTROL").update({"buzzer": "1"})
                    timeout = (datetime.now() + timedelta(seconds=washTime)
                               ).time()  #loop time = washTime
                    timeout = datetime.combine(date.today(), timeout)
                    db1.child("main").update(
                        {"console": "Washing for {}s...".format(washTime)})
                    while True:
                        updSensor("sound", "sound")
                        if (datetime.now() > timeout):
                            break
                    db2.child("PI_03_CONTROL").update({"buzzer": "0"})
                    db1.child("main").update(
                        {"console": "Finished washing..."})
                    spokenCommand, isDefault = speechToText()
                else:
                    break

            #flushing
            flushTime = int(
                spokenCommand.split(' ')[2]) if not isDefault else 15
            db2.child("PI_03_CONTROL").update({"ledlgt": "1"})
            timeout = (datetime.now() + timedelta(seconds=flushTime)).time()
            timeout = datetime.combine(date.today(), timeout)
            db1.child("main").update(
                {"console": "Flushing for {}s...".format(flushTime)})
            while True:
                updSensor("light", "led")
                if (datetime.now() > timeout):
                    break
            db2.child("PI_03_CONTROL").update({"ledlgt": "0"})
            outputConsole("Finished flushing...")

            #display time actually spent pooing or urinating
            lcdColor = {
                "lcdbkR": str(0),
                "lcdbkG": str(5),
                "lcdbkB": str(0),
            }
            db2.child("PI_03_CONTROL").update(lcdColor)
            peepooTime = str(peepooTime)
            if (len(peepooTime) == 2):  # Used 10 to 99 seconds
                db2.child("PI_03_CONTROL").update(
                    {"lcdtxt": "Time spent = " + peepooTime + "s"})
            elif (len(peepooTime) == 1):
                db2.child("PI_03_CONTROL").update(
                    {"lcdtxt": "Time spent =  " + peepooTime + "s"})
            else:  # Used 100 to 999 seconds
                db2.child("PI_03_CONTROL").update(
                    {"lcdtxt": "Time spent= " + peepooTime + "s"})
            outputConsole("Displaying time spent...")

            sleep(2)
            takePic("lcdTime",
                    "lt")  # Take picture of time spent for pee or poo on lcd

            data = {
                "relay1": str(0),
                "relay2": str(0),
            }

            outputConsole("User may leave...")
            #detect user leaving & present report afterwards
            while True:
                if (300 > 200):
                    db2.child("PI_03_CONTROL").update(data)
                    takePic("userOut", "uo")  # Take pictures of relays off
                    break
            outputConsole("User has left...")

            #TODO
            #detect poo/urine type based on pi image
            wastageType = findType("wastage.jpg")
            db1.child("main").child(day).child(count).update(
                {"wastageType": wastageType})
            outputConsole("Wastage type & color detected: {}...".format(wastageType))

            #give recommendations to user based on that
            if (day != strftime("%Y%m%d", localtime()) or stop_run):
                generateReport(day)

            #integrate python with javascript & deploy
            #data stored:
            #ultra1, ultra2, sound, light, time, wastagetype
            global c
            c += 1
            count = str(f'{c:02}')
        except KeyboardInterrupt:
            exit


def manual_run():
    t = Thread(target=run)
    t.start()
    return index()


@app.route("/run/", methods=['GET'])
def run_process():
    global stop_run
    stop_run = False
    return Response(manual_run(), mimetype="text/html")


@app.route("/stop/", methods=['GET'])
def set_stop_run():
    global stop_run
    stop_run = True
    return index()


if __name__ == '__main__':
    app.run(debug=True)
