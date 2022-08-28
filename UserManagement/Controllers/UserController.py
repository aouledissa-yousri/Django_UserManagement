from Test.settings import SECRET_KEY
from UserManagement.Controllers.TokenController import TokenController
from ..extra import *
from ..models import GenericUser
import jwt

class UserController: 

    #delete account
    @staticmethod 
    def deleteAccount(request):
        #get request data
        data = getRequestBody(request)

        try: 
            #search for user and delete it

            GenericUser.objects.filter(username = data["username"]).delete()
            return {"message": "user has beeen deleted"}
        
        except GenericUser.DoesNotExist: 
            #if user does not exist
            return {"message": "user does not exist"}
    

    #log out 
    @staticmethod 
    def logout(request):
        TokenController.deleteToken(request.headers["Token"])
        return {"message": "logged out"}
