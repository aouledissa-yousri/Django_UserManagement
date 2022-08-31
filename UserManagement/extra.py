from UserManagement.models import *
from .Controllers.LocationController import LocationController
from datetime import datetime, timedelta
import json, random, secrets, string, requests, pytz

#get resuest body
def getRequestBody(request):
    return json.loads(request.body) 

#generate random confirmation/verification code
def generateCode():
    n = random.randint(6,10)
    res = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(n))
    return res

#get base url 
def getBaseUrl(request):
    baseUrl = str(request.build_absolute_uri()).replace(request.path, "")
    return baseUrl

#generate expiration date based on country 
def generateExpirationDate(request):
    response = json.loads(requests.get(f"https://ipinfo.io/{LocationController.getUserIp(request)}/json").content)
    if response["ip"] == "127.0.0.1":
        return datetime.now() + timedelta(minutes=5)
    return datetime.now(pytz.timezone(response["timezone"])) + timedelta(minutes=5)










