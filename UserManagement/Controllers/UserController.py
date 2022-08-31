from UserManagement.Controllers.TokenController import TokenController
from ..extra import *
from ..models.GenericUser import GenericUser
from ..models.Token import Token

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


    #logout from all sessions 
    @staticmethod 
    def logoutAllSessions(request):
        decodedToken = TokenController.decodeToken(request.headers["Token"])

        try: 
            user = User.objects.get(id = decodedToken["id"])
            Token.objects.filter(user_id = user.id).delete()
            return {"message": "logged out from all sessions"}
        
        except User.DoesNotExist: 
            return {"message": "user not found"}
    

    @staticmethod 
    def logoutAllOtherSessions(request):
        decodedToken = TokenController.decodeToken(request.headers["Token"]) 

        try: 
            user = User.objects.get(id = decodedToken["id"])
            Token.objects.filter(user_id = user.id).exclude(token = request.headers["Token"]).delete()
            return {"message": "logged out from all other sessions"}
        
        except User.DoesNotExist: 
            return {"message": "user not found"}

