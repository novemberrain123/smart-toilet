from main import outputConsole
import math
from pyrebase import pyrebase
import numpy as np

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

timeList = [70, 55, 31, 64, 45, 66, 72, 59]
typeList = ['pee_yellow', 'pee_yellow', 'pee_yellow', 'poo_black', 'pee_yellow', 'pee_yellow', 'poo_black', 'pee_yellow', 'pee_yellow', 'poo_black']
normalPeePooTime = 60
normalPeeCount = 7
normalPooCount = 1
peeCount = 0
pooCount = 0
totalScore = 0
averagePeePooTime = np.mean(timeList)


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