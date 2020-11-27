from time import *
from pyrebase import pyrebase
from datetime import *
import urllib.request, json
import random
import speech_recognition as sr
import pyttsx3
import pyaudio
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
config2 = {
    "apiKey": "AIzaSyAs_1NVtsjZ-LmTATAp0a0R5fK6XdKHaMU",
    "authDomain": "bait2123-202010-03.firebaseapp.com",
    "databaseURL": "https://bait2123-202010-03.firebaseio.com/",
    "storageBucket": "bait2123-202010-03.appspot.com"
}

firebase2 = pyrebase.initialize_app(config2)
auth2 = firebase2.auth()
user2 = auth2.sign_in_with_email_and_password("bait2123.iot.03@gmail.com",
                                              "BeyondEducationH03")
db2 = firebase2.database()
storage2 = firebase2.storage()

c = 0  #subfolder initialization
r = sr.Recognizer()


def takePic():
    db2.child("PI_03_CONTROL").update({"camera": str(1)})
    print(str(datetime.now()))
    sleep(10)
    print(str(datetime.now()))
    db2.child("PI_03_CONTROL").update({"camera": str(0)})


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
        db1.child("main").child(c).update(
            {ultName: str(ultResults)})  #write ultrasensor results to db1
        return float(ultResults)


def updSensor(input, output):
    y, hour, date = getLatestSubfolder()
    for keyValue in y:
        x = str(keyValue.key())
        results = db2.child("PI_03_" + date).child(hour).child(x).child(
            input).get().val()
        db1.child("main").child(c).update({output: str(results)})


def speechToText():
    wash_v = ["wash", "war", "lasts",
                  "watch"]  #list of words meant to mean wash
    flush_v = ["flush","flash","lush","slush","flourish"]
    while True:
        try:
            with sr.Microphone() as source2:

                r.adjust_for_ambient_noise(source2, duration=0.2)

                #listens for the user's input
                audio2 = r.listen(source2)

                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()

                if (MyText.split(' ')[0] in (wash_v or flush_v) and MyText.split(' ')[3].isdigit()):
                    print(MyText)
                    return MyText
                else:
                    print("Please repeat your command")
            

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("Please repeat")


while True:
    try:
        data = {
            "relay1": str(
                1
            ),  #red light & white light == on, blue light & green light == off
            "relay2": str(1),
        }
        while True:
            if (
                    1 <= 20
            ):  #if user detected turn relay1 and relay2 on correct: updUltsensor("ultra1")
                db2.child("PI_03_CONTROL").update(data)
                break
            sleep(9)

        #takePic()

        check = True
        beginTime = perf_counter()
        while check:
            if (updUltsensor("ultra2") <= 20):
                beginTime = perf_counter()
                while check:
                    if (updUltsensor("ultra2") > 20):
                        secondTime = perf_counter()
                        while check:
                            if (updUltsensor("ultra2") > 20):
                                if ((perf_counter() - secondTime) > 20):
                                    check = False
                            else:
                                break
        overallTime = perf_counter() - beginTime
        db1.child("main").child(c).update({"overallTime": str(overallTime)
                                           })  #update time to main db

        #random image is chosen and displayed
        bin = [
            "pee_clear", "pee_yellow", "pee_pink", "poo_black", "poo_brown",
            "poo_yellow"
        ]
        randS = "E:\Code\smart-toilet\img\\" + random.choice(bin) + ".png"
        storage2.child("image/oled.jpg").put(randS)
        db2.child("PI_03_CONTROL").update({"oledsc": "1"})

        #picture taken
        takePic()

        spokenCommand = speechToText()
        wash_v = ["wash", "war", "lasts",
                  "watch"]  #list of words meant to mean wash
        if (spokenCommand.split(' ')[0] in wash_v):
            washTime = int(spokenCommand.split(' ')[2])
            db2.child("PI_03_CONTROL").update({"buzzer": "1"})
            timeout = time() + washTime #loop time = washTime
            while True:
                updSensor("sound","sound")
                if(time()>timeout):
                    break
            
            else:

        break
    except KeyboardInterrupt:
        exit