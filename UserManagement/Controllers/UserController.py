from threading import Thread
from UserManagement.Controllers.ConfirmationCodeController import ConfirmationCodeController
from ..serializers import UserSerializer
from ..models import ConfirmationCode, User
from ..classes.Credentials import Credentials
from Test.settings import SECRET_KEY
from django.utils import timezone
from ..extra import *
import jwt



class UserController: 

    @staticmethod
    def signUp(request, template = None):
        userData = getRequestBody(request)
        user = User()
        user.setData(userData)
        user = UserSerializer(data = user.getAllUserData())
        if user.is_valid():
            user.save()
            ConfirmationCodeController.sendConfirmationEmail(userData, template)
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
           
    
    @staticmethod 
    def checkPasswordResetCode(request):
        code = getRequestBody(request)["code"]
        try:
            passwordResetCode = PasswordResetCode.objects.get(code = code)
            if passwordResetCode.expirationDate >= timezone.now():
                return {
                    "message": "Password code is valid",
                    "user": User.objects.get(id = passwordResetCode.user.id).getData()
                }
            return "Password reset code has been expired"
        except PasswordResetCode.DoesNotExist:
            return "Password reset code is not valid"
    
    @staticmethod 
    def resetPassword(request):
        userData = getRequestBody(request)
        try: 
            user =User.objects.get(username = userData["username"])
            user.changePassword(userData["password"])
            return "Password has been changed"

        except User.DoesNotExist:
            return "Invalid username"

    @staticmethod 
    def changeUsername(request):
        userData = getRequestBody(request)
        try: 
            User.objects.get(username = userData["newUsername"])
            return "Username provided already exists"
        
        except User.DoesNotExist: 
            try:
                User.objects.get(username = userData["oldUsername"]).updateUsername(userData["newUsername"])
                return "Username has been changed"
            
            except User.DoesNotExist:
                return "invalid user"
            

    
        


