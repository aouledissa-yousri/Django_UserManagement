from Test.settings import SECRET_KEY
from UserManagement.models import Token
from django.http import JsonResponse
import jwt

#check if access token is valid or not when making a post request to the server
def checkAccessToken(func, algorithm="HS512"):
    
    def wrapper(request, *args, **kwargs):
        try: 
            _token = request.headers["Token"]
            try:
                jwt.decode(_token, SECRET_KEY, algorithms = [algorithm])

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
