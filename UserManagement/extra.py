from UserManagement.models import *
import json, random, secrets, string


def getRequestBody(request):
    return json.loads(request.body) 

#generate random confirmation/verification code
def generateCode():
    n = random.randint(6,10)
    res = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(n))
    return res









