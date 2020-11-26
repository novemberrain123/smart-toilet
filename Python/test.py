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
    scd = str(datetime.now())[-9:]
    sleep(10)
    print(str(datetime.now()))
    db2.child("PI_03_CONTROL").update({"camera":str(0)})
    return scd
while True:
    try:
        takePic()
        ImgUrl = storage2.child("PI_03_CONTROL/cam_20201125123350.jpg").get_url(user1['idToken'])
        ImgUrl1 = storage2.child("PI_03_CONTROL/cam_2020112512335.jpg").get_url(user1['idToken'])
        print(len(ImgUrl))
        print(len(ImgUrl1))
        break
    except KeyboardInterrupt: 
        exit