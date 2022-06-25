from Test.settings import SECRET_KEY
from UserManagement.models import *
from django.http import JsonResponse
import json, jwt

def getRequestBody(request):
    return json.loads(request.body) 


def checkAccessToken(func, algorithm="HS512"):
    
    def wrapper(request, *args, **kwargs):
        token = request.headers["Token"]
        try:
            decodedToken = jwt.decode(token, SECRET_KEY, algorithms = [algorithm])

            try:
                User.objects.get(username = decodedToken["username"])   
                return func(request, *args, **kwargs)
                
            except User.DoesNotExist:
                return JsonResponse({"response": "invalid token"})

        except jwt.exceptions.DecodeError:
            return JsonResponse({"response": "invalid token"})
    return wrapper


