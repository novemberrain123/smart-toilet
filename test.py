from main import takePic
from time import *
from pyrebase import pyrebase
from datetime import *
import random
from pathlib import Path
    
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
    "storageBucket": "bait2123-202010-03.appspot.com",
    "serviceAccount": ".vscode/bait2123-202010-03-firebase-adminsdk-xmqwi-1caf6b0286.json"
}

firebase2 = pyrebase.initialize_app(config2)
auth2 = firebase2.auth()
user2 = auth2.sign_in_with_email_and_password("bait2123.iot.03@gmail.com", "BeyondEducationH03")
db2 = firebase2.database()
storage2 = firebase2.storage()

while True:
    try:
        #random image is chosen and displayed
        cwd = str(Path.cwd())
        cwd = '/'.join(cwd.split('\\'))
        print(cwd)
        bin = [
            "pee_clear", "pee_yellow", "pee_pink", "poo_black", "poo_brown",
            "poo_yellow"
        ]
        randS = cwd + "/img/poo_black.png"
        storage2.child("images/oled.jpg").put(randS)
        db2.child("PI_03_CONTROL").update({"oledsc": "1"})
        sleep(10)
        takePic()
        db2.child("PI_03_CONTROL").update({"oledsc": "0"})
        break
    except KeyboardInterrupt: 
        exit