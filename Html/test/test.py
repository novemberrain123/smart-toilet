import sys
import json
import requests

url= "http://opensourcepyapi.herokuapp.com:443/weather/06604"
requests.get(url)
data =r.json()
resp = {
    "Response":200,
    "Message":"Data From Python",
    "Data":data
}


print(json.dumps(resp))

sys.stdout.flush()
