from threading import Thread
from UserManagement.Controllers.ConfirmationCodeController import ConfirmationCodeController
from UserManagement.Controllers.TwoFactorAuthCodeController import TwoFactorAuthCodeController
from UserManagement.Controllers.TokenController import TokenController
from ..serializers import GenericUserSerializer
from ..models import ConfirmationCode, GenericUser
from ..classes.Credentials import Credentials
from Test.settings import SECRET_KEY
from django.utils import timezone
from django.shortcuts import redirect
from ..extra import *
import jwt



class GenericUserController: 


    #create new account
    @staticmethod
    def signUp(request, template = None):
        userData = getRequestBody(request)
        user = GenericUser()
        user.setData(userData)
        user = GenericUserSerializer(data = user.getAllUserData())
        if user.is_valid():
            user.save()
            ConfirmationCodeController.sendConfirmationEmail(userData, template)
            return "Account created successfully now you need to verify your account"
        try:
            GenericUser.objects.get(username = userData["username"])
            return "Account already exists"
        except GenericUser.DoesNotExist:
            return "Account creation failed"


    #login to an existing account
    @staticmethod 
    def login(data, passwordFromUser = True):
        try: 

            #serach for user in database 
            credentials = Credentials(data, passwordFromUser)
            account = GenericUser.login(credentials)

            #if username (or email) and password are correct get user data and access token 
            if account.password == credentials.getPassword() and (not account.isBlocked()):
                if not account.verified: 
                    ConfirmationCodeController.sendConfirmationEmail(account.getData(), None)
                    return {"message": "You need to verify your account"}

                account.restartTries()

                token = TokenController.generateToken({
                    "username": account.username,
                    "number": random.randint(0, 10000000000000000)
                })

                TokenController.saveToken(token)

                return {
                    "message": "success",
                    "user": account.getData(),
                    "token": token
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
        except GenericUser.DoesNotExist : 
            return {"message":"user not found"}
    

    #log out 
    @staticmethod 
    def logout(request):
        data = getRequestBody(request)
        TokenController.deleteToken(data["token"])
        return {"message": "logged out"}
    
    #login withoput 2-step verification
    @staticmethod 
    def normalLogin(data):
        return GenericUserController.login(data)


    #check verification code
    @staticmethod 
    def twoFactorAuthLogin(request):
        data = getRequestBody(request)
        try:
            user = GenericUser.objects.get(username = data["username"])
            try:
                code = data["verificationCode"]
                del code
                try:
                    twoFactorAuthCode = TwoFactorAuthCode.objects.get(code = data["verificationCode"], user_id=user.id)
                    if twoFactorAuthCode.expirationDate >= timezone.now():
                        twoFactorAuthCode.delete()
                        return GenericUserController.login(user.getAllUserData(), False)
                    return {"message":"Verification code has been expired"}
                except TwoFactorAuthCode.DoesNotExist:
                    return {"message":"Verification code is not valid"}

            except KeyError: 
                return {"message":"Verification code has not been provided"}
        except GenericUser.DoesNotExist:
            return {"message": "User not found"}
    
    #login with 2-step verification code
    @staticmethod 
    def loginGateway(request):
        data = getRequestBody(request)
        try: 
            user = User.objects.get(username = data["username"])
            if user.twoFactorAuth:
                data["email"] = user.email
                return {"message": TwoFactorAuthCodeController.sendTwoFactorAuthCode(data)}
            return GenericUserController.normalLogin(data)
        except User.DoesNotExist:
            return {"message" : "User not found"}
        except KeyError:
            return {"message": "Invalid username and email"}

    
    
    #verify account
    @staticmethod 
    def confirmAccount(request):
        data = getRequestBody(request)
        user = GenericUser.objects.get(username = data["username"])
        try:
            confirmationCode = ConfirmationCode.objects.get(code = data["code"], user_id = user.id)
            if confirmationCode.expirationDate >= timezone.now():
                user.verify()
                confirmationCode.delete()
                return GenericUserController.login(user.getAllUserData(), False)
            return "Confirmation code has been expired"
        except ConfirmationCode.DoesNotExist:
            return "Confirmation code is not valid"
           
    
    #check password reset code
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
    
    #reset password
    @staticmethod 
    def resetPassword(request):
        userData = getRequestBody(request)
        try: 
            user =GenericUser.objects.get(username = userData["username"])
            user.changePassword(userData["password"])
            return "Password has been changed"

        except GenericUser.DoesNotExist:
            return "Invalid username"

    #change username
    @staticmethod 
    def changeUsername(request):
        userData = getRequestBody(request)
        try: 
            GenericUser.objects.get(username = userData["newUsername"])
            return {"message":"Username provided already exists"}
        
        except GenericUser.DoesNotExist: 
            try:
                GenericUser.objects.get(username = userData["oldUsername"]).updateUsername(userData["newUsername"])
                return {
                    "message ": "Username has been changed",
                    "token": GenericUserController.generateToken({
                        "username": userData["newUsername"]
                    })
                }
            
            except GenericUser.DoesNotExist:
                return {"message":"invalid user"}
    

    
            

   
    
        


