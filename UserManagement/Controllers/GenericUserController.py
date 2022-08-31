from threading import Thread
from UserManagement.Controllers.ConfirmationCodeController import ConfirmationCodeController
from UserManagement.Controllers.TwoFactorAuthCodeController import TwoFactorAuthCodeController
from UserManagement.Controllers.TokenController import TokenController
from ..serializers import GenericUserSerializer
from ..models.ConfirmationCode import ConfirmationCode
from ..models.GenericUser import GenericUser 
from ..classes.Credentials import Credentials
from django.utils import timezone
from ..extra import *



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
            #ConfirmationCodeController.sendConfirmationEmail(userData, request, template)
            return "Account created successfully now you need to verify your account"
        try:
            GenericUser.objects.get(username = userData["username"])
            return "Account already exists"

        except GenericUser.DoesNotExist:
            return "Account creation failed"
        
        except KeyError: 
            return "Invalid parameters"


    #login to an existing account
    @staticmethod 
    def login(data, request = None, passwordFromUser = True):
        try: 

            #serach for user in database 
            credentials = Credentials(data, passwordFromUser)
            account = GenericUser.login(credentials)
            print(data["password"])
            print("credentials password: " + credentials.password)
            print("account password: " + account.password)

            #if username (or email) and password are correct get user data and access token 
            if account.password == credentials.getPassword() and (not account.isBlocked()):
                if not account.verified: 
                    ConfirmationCodeController.sendConfirmationEmail(account.getData(), request)
                    return {"message": "You need to verify your account"}

                account.restartTries()

                token = TokenController.generateToken({
                    "username": account.username,
                    "id": account.id,
                    "number": random.randint(0, 10000000000000000)
                })

                TokenController.saveToken(token, account)

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
        
        except KeyError: 
            return {"message": "invalid parameters"}
    
    
    #login withoput 2-step verification
    @staticmethod 
    def normalLogin(data, request):
        return GenericUserController.login(data, request)
    
    #enable two factor authentication
    @staticmethod 
    def manageTwoFactorAuth(request):
        data = getRequestBody(request)

        #search for user 
        try: 
            if "enableTwoFactorAuth" in request.path:
                GenericUser.objects.filter(username = data["username"]).update(twoFactorAuth = True)
                return {"message": "2 factor authentication enabled"}

            elif "disableTwoFactorAuth" in request.path:
                GenericUser.objects.filter(username = data["username"]).update(twoFactorAuth = False)
                return {"message": "2 factor authentication disabled"}
        
        except GenericUser.DoesNotExist: 
            return {"message": "user does not exist"}
        
        except KeyError: 
            return {"message": "Invalid parameters"}
    


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
            user = GenericUser.objects.get(username = data["username"])
            data["email"] = user.email
            
        except GenericUser.DoesNotExist:
            return {"message" : "User not found"}
       
        except KeyError:
            try: 
                user = GenericUser.objects.get(email = data["email"])
                data["username"] = user.username

            except KeyError: 
                return {"message": "Invalid username or email"}
            
            except GenericUser.DoesNotExist:
                return {"message" : "User not found"}
        
        if user.twoFactorAuth:
            return {"message": TwoFactorAuthCodeController.sendTwoFactorAuthCode(data, request)}
        return GenericUserController.normalLogin(data, request)

    
    
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
                print("user password :"+ user.getAllUserData()["password"])
                return GenericUserController.login(user.getAllUserData(), passwordFromUser = False)
            return {"message": "Confirmation code has been expired"}

        except ConfirmationCode.DoesNotExist:
            return {"message": "Confirmation code is not valid"}
        
        except KeyError: 
            return {"message": "Invalid parameters"}
           
    
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
        
        except KeyError:
            return "Invalid parameters"
    
    #reset password
    @staticmethod 
    def resetPassword(request):
        userData = getRequestBody(request)
        try: 
            user = GenericUser.objects.get(username = userData["username"])
            user.changePassword(userData["password"])
            return "Password has been changed"

        except GenericUser.DoesNotExist:
            return "Invalid username"
        
        except KeyError:
            return "Invalid parameters"

    #change username
    @staticmethod 
    def changeUsername(request):
        userData = getRequestBody(request)
        try: 
            #check if username exists
            GenericUser.objects.get(username = userData["newUsername"])
            return {"message":"Username provided already exists"}
        
        except GenericUser.DoesNotExist: 
            try:
                #change username and delete old access token
                GenericUser.objects.get(username = userData["oldUsername"]).updateUsername(userData["newUsername"])
                Token.objects.filter(token = request.headers["Token"]).delete()

                token = TokenController.generateToken({
                    "username": userData["newUsername"],
                    "number": random.randint(0, 10000000000000000)
                })

                TokenController.saveToken(token, GenericUser.objects.get(username = userData["newUsername"]))


                return {
                    "message ": "Username has been changed",
                    "username": userData["newUsername"],
                    "token": token
                }
            
            except GenericUser.DoesNotExist:
                return {"message":"invalid user"}
        
        except KeyError: 
            return {"message": "invalid parameters"}
    

    
    
