from Test.settings import SECRET_KEY
from UserManagement.models import *
from django.http import JsonResponse
import json, jwt, random, secrets, string


def getRequestBody(request):
    return json.loads(request.body) 


#check if access token is valid or not when making a post request to the server
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
                
                except Token.DoesNotExist:
                    return JsonResponse({"response": "invalid token"})

            except jwt.exceptions.DecodeError:
                return JsonResponse({"response": "invalid token"})

        except KeyError: 
            return JsonResponse({"response": "invalid token"})

    return wrapper


#generate random confirmation/verification code
def generateCode():
    n = random.randint(6,10)
    res = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(n))
    return res




