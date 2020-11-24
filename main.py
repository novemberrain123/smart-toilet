from time import *
from pyrebase import pyrebase
from datetime import *

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
config2 = {
    "apiKey": "AIzaSyAs_1NVtsjZ-LmTATAp0a0R5fK6XdKHaMU",
    "authDomain": "bait2123-202010-03.firebaseapp.com",
    "databaseURL": "https://bait2123-202010-03.firebaseio.com/",
    "storageBucket": "bait2123-202010-03.appspot.com"
}

firebase2 = pyrebase.initialize_app(config2)
auth2 = firebase2.auth()
user2 = auth2.sign_in_with_email_and_password("bait2123.iot.03@gmail.com", "BeyondEducationH03")
db2 = firebase2.database()
storage2 = firebase2.storage()
c = 0
def takePic():
    db2.child("PI_03_CONTROL").update({"camera":str(1)})
    print(str(datetime.now()))
    sleep(10)
    print(str(datetime.now()))
    db2.child("PI_03_CONTROL").update({"camera":str(0)})
while True:
    try:
        Hour = str(datetime.now())[11:13]
        date = strftime("%Y%m%d", localtime()) 

        #Get the last child for the last sensor record which is Minute+Second, which is y
        
        y = db2.child("PI_03_" + date).child(Hour).order_by_key().limit_to_last(1).get()
        for keyValue in y:
            x = str(keyValue.key())
            ultResults = db2.child("PI_03_" + date).child(Hour).child(x).child("ultra").get().val()
            print(ultResults)
            print("The path is > PI_03_"+date+" > "+Hour+" > "+x)
        #record every 10 secs
        db1.child("main").child(c).update({"ultra":str(ultResults)}) #write ultrasensor results to db1
        data = {
            "relay1":str(1), #red light & white light == on, blue light & green light == off
            "relay2":str(1),
        }
        data1 = {
            "relay1":str(0),
            "relay2":str(0),
        }
        ultResults = 1 # test
        if (ultResults<=20): #if user detected turn relay1 and relay2 on
            db2.child("PI_03_CONTROL").update(data)
        
        sleep(0.5)

        takePic()

        ImgUrl = storage2.child("PI_03_CONTROL/cam_2020112421311.jpg").download("E:\Code\smart-toilet","imga.jpg")
        print(ImgUrl)
        break
    except KeyboardInterrupt: 
        exit