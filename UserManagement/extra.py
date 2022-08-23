from Test.settings import SECRET_KEY
from UserManagement.models import *
from django.http import JsonResponse
import random, secrets, string
import json, jwt

def getRequestBody(request):
    return json.loads(request.body) 


def checkAccessToken(func, algorithm="HS512"):
    
    def wrapper(request, *args, **kwargs):
        try: 
            _token = request.headers["Token"]
            try:
                decodedToken = jwt.decode(_token, SECRET_KEY, algorithms = [algorithm])

                try:
                    #User.objects.get(username = decodedToken["username"])   
                    Token.objects.get(token = _token)
                    return func(request, *args, **kwargs)
                
                except User.DoesNotExist:
                    return JsonResponse({"response": "invalid token"})

            except jwt.exceptions.DecodeError:
                return JsonResponse({"response": "invalid token"})

        except KeyError: 
            return JsonResponse({"response": "invalid token"})

    return wrapper


def generateCode():
    n = random.randint(6,10)
    res = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(n))
    return res


