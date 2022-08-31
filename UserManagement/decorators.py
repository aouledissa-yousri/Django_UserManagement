from Test.settings import SECRET_KEY
from UserManagement.models.Token import Token
from UserManagement.models.GenericUser import GenericUser
from .Controllers.LocationController import LocationController
from .Controllers.LocationCodeController import LocationCodeController
from .Controllers.TokenController import TokenController
from django.http import JsonResponse
from .extra import *
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


#check if location is valid 
def checkUserLocation(func):

    def wrapper(request, *args, **kwargs):
        
        #check verified user locations
        verifiedLocations = LocationController.getVerifiedLocations(request)


        #verify location if there are no other verified locations
        if verifiedLocations["location number"] == 0: 
            if LocationController.addNewLocationToUser(request):
                return func(request, *args, **kwargs)
            
            return {"message": "an unknwon error occurred please try again later"}
        
        #check if location is verified
        try:
            verifiedLocations["locations"].get(ip = LocationController.getUserIp(request))
            return func(request, *args, **kwargs)

        #send location verification email
        except Location.DoesNotExist:
            try:
                LocationCodeController.sendLocationVerificationEmail(GenericUser.objects.get(id = TokenController.decodeToken(request.headers["Token"])["id"]).getData(), request, getBaseUrl(request))
                return {"message": "a verification link has been sent to your email"}
            
            except GenericUser.DoesNotExist: 
                return {"message": "User not found"}
    
    return wrapper
