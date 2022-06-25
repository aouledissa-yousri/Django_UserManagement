from threading import Thread
from UserManagement.Controllers.ConfirmationCodeController import ConfirmationCodeController
from ..serializers import UserSerializer
from ..models import ConfirmationCode, User
from ..classes.Credentials import Credentials
from Test.settings import SECRET_KEY
from django.template.loader import render_to_string
from django.utils import timezone
from ..extra import *
import jwt



class UserController: 

    @staticmethod
    def signUp(request):
        userData = getRequestBody(request)
        user = User()
        user.setData(userData)
        confirmationCode = ConfirmationCodeController.generateConfirmationCode()
        user = UserSerializer(data = user.getAllUserData())
        if user.is_valid():
            user.save()
            ConfirmationCodeController.sendConfirmationEmail(userData, confirmationCode)
            return "Account created successfully now you need to verify your account"
        try:
            User.objects.get(username = userData["username"])
            return "Account already exists"
        except User.DoesNotExist:
            return "Account creation failed"
    
    @staticmethod 
    def login(request):
        try: 
            data = getRequestBody(request)

            #serach for user in database 
            credentials = Credentials(data)
            account = User.login(credentials)

            #if username (or email) and password are correct get user data and access token 
            if account.password == credentials.getPassword() and (not account.isBlocked()):
                if not account.verified: 
                    return {"message": "You need to verify your account"}

                account.restartTries()
                return {
                    "message": "success",
                    "user": account.getData(),
                    "token": UserController.generateToken({
                        "username": account.username,
                    })
                }
            
            
            
            #if password is wrong decrement login possible attempts
            account.decrementTries()

            #if user provides a wrong password for the third time block his account for a specefic period of time
            if account.getTries() < 1 :
                if not account.isBlocked():
                    account.block()
                    Thread(target = account.unblock).start()

                #if account is blocked temporarily
                return {"message": "your account is temporarily blocked please try again later!"}

            #if password is wrong
            return {"message":"password is wrong"}
        
        #if user is not found
        except User.DoesNotExist : 
            return {"message":"user not found"}
    

    @staticmethod 
    def generateToken(payload):
        return jwt.encode(payload, SECRET_KEY, algorithm = "HS512")
    
    @staticmethod 
    def confirmAccount(request):
        data = getRequestBody(request)
        try:
            #if checkAccessToken(request.headers["Token"]) == "valid token":
            user = User.objects.get(username = data["username"])
            try:
                confirmationCode = ConfirmationCode.objects.get(code = data["code"], user_id = user.id)
                if confirmationCode.expirationDate >= timezone.now():
                    user.verify()
                    confirmationCode.delete()
                    return "Confirmation code is valid"
                return "Confirmation code has been expired"
            except ConfirmationCode.DoesNotExist:
                return "Confirmation code is not valid"
            #else: 
                #return "invalid token"
        except KeyError: 
            return "invalid token"

    
    @staticmethod 
    def checkAccessToken(token):
        try:
            decodedToken = jwt.decode(token, SECRET_KEY, algorithms = ["HS512"])

            try:
                User.objects.get(username = decodedToken["username"])        
                return "valid token"
            except User.DoesNotExist:
                return "invalid token"

        except jwt.exceptions.DecodeError:
            return "invalid token"
    

    
        


