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
    "storageBucket": "bait2123-202010-03.appspot.com",
    "serviceAccount": ".vscode/bait2123-202010-03-firebase-adminsdk-xmqwi-1caf6b0286.json"
}

firebase2 = pyrebase.initialize_app(config2)
auth2 = firebase2.auth()
user2 = auth2.sign_in_with_email_and_password("bait2123.iot.03@gmail.com", "BeyondEducationH03")
db2 = firebase2.database()
storage2 = firebase2.storage()

def takePic():
    db2.child("PI_03_CONTROL").update({"camera":str(1)})
    print(str(datetime.now()))
    sleep(10)
    print(str(datetime.now()))
    db2.child("PI_03_CONTROL").update({"camera":str(0)})

while True:
    try:
        all_files = storage2.child("PI_03_CONTROL").list_files()
        for file in all_files:            
            try:
                print(file.name)
                print(storage2.child(file.name).get_url())
                break
            except:    
                print('Download Failed')   
        break
    except KeyboardInterrupt: 
        exit