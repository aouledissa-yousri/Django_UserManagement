from ..models.GenericUser import GenericUser
from ..models.Location import Location
from ..models.LocationCode import LocationCode
from .TokenController import TokenController
from ..serializers import LocationSerializer
from django.utils import timezone
from ..extra import *


class LocationController: 

    #get user's IP address
    @staticmethod 
    def getUserIp(request):
        xForwardedFor = request.META.get('HTTP_X_FORWARDED_FOR')
    
        if xForwardedFor:
            ip = xForwardedFor.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        return ip
    
    #add new verified location
    @staticmethod 
    def addNewLocationToUser(request): 
        ip = LocationController.getUserIp(request)

        try: 
            user = GenericUser.objects.get(username = TokenController.decodeToken(request.headers["Token"])["username"])

            location = Location()
            location.setData(ip, user)
            location = LocationSerializer(data = location.getData())

            if location.is_valid():
                location.save()
                return True
            
            return False
        
        except GenericUser.DoesNotExist:
            return False
    
    #search location in database
    @staticmethod 
    def searchLocation(request):
        ipAddress = LocationController.getUserIp(request)

        try: 
            Location.objects.get(ip = ipAddress)
            return True 
        
        except Location.DoesNotExist: 
            return False  


    #get verified locations
    @staticmethod 
    def getVerifiedLocations(request): 

        locations = Location.objects.filter(user_id =   TokenController.decodeToken(request.headers["Token"])["id"])

        result = {
            "location number": locations.count()
        }

        if locations.count() > 0: 
            result["locations"] = locations
            
        return result
    

    #verify new location 
    @staticmethod 
    def verifyNewLocation(request):
        if "?code=" in request.build_absolute_uri():
            locationCode = request.build_absolute_uri().split("=")[1]
            
            try: 
                locationCode = LocationCode.objects.get(code = locationCode)
                if locationCode.expirationDate >= timezone.now():

                    if LocationController.addNewLocationToUser(request): 
                        return {"message": "location has been verified"}

                return {"message": "verification link has been expired"}
            
            except LocationCode.DoesNotExist: 
                return {"message": "invalid verification link"}
        
        return {"message": "invalid request"}

            
        

        
            

