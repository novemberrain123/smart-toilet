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


while True:
    try:
        Hour = str(datetime.now())[11:13]
        date = strftime("%Y%m%d", localtime()) 

        #Get the last child for the last sensor record which is Minute+Second, which is y
        
        y = db2.child("PI_03_" + date).child(Hour).order_by_key().limit_to_last(1).get()
        for keyValue in y:
            x = str(keyValue.key())
            ultResults = db2.child("PI_03_" + date).child(Hour).child(x).child("ultra").get()
            print(ultResults.val())
            print("The path is > PI_03_"+date+" > "+Hour+" > "+x)

        break
    except KeyboardInterrupt: 
        exit