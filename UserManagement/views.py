from tabnanny import check
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from UserManagement.Controllers.FacebookUserController import FacebookUserController
from UserManagement.Controllers.GoogleUserController import GoogleUserController
from UserManagement.Controllers.ConfirmationCodeController import ConfirmationCodeController
from UserManagement.Controllers.GenericUserController import GenericUserController
from UserManagement.Controllers.PasswordResetCodeController import PasswordResetCodeController
from UserManagement.Controllers.UserController import UserController
from UserManagement.extra import *
from UserManagement.decorators import *

# Create your views here.

#user normal sign up
@api_view(["POST"])
def signUp(request):
    return JsonResponse({"signed up": GenericUserController.signUp(request)})

#user login
@api_view(["POST"])
def login(request):
    return JsonResponse(GenericUserController.loginGateway(request))

#google login gateway 
@api_view(["GET"])
def googleLoginGateway(request):
    return JsonResponse(GoogleUserController.googleLoginGateway())

#google login
@api_view(["GET"])
def googleLogin(request):
    return JsonResponse(GoogleUserController.googleLogin(request))

#facebook login gateway
@api_view(["GET"])
def facebookLoginGateway(request):
    return JsonResponse(FacebookUserController.facebookLoginGateway())

#facebook login
@api_view(["GET"])
def facebookLogin(request):
    return FacebookUserController.facebookLogin(request)


#user logout
@api_view((["POST"]))
@checkAccessToken
def logout(request):
    return JsonResponse(UserController.logout(request))

#logout from all sessions
@api_view((["POST"]))
@checkAccessToken
def logoutAllSessions(request):
    return JsonResponse(UserController.logoutAllSessions(request))

#logout from all other sessions
@api_view((["POST"]))
@checkAccessToken
def logoutAllOtherSessions(request):
    return JsonResponse(UserController.logoutAllOtherSessions(request))


#enable 2 factor authentication
@api_view(["POST"])
@checkAccessToken
def enableTwoFactorAuth(request):
    return JsonResponse(GenericUserController.manageTwoFactorAuth(request))

#disable 2 factor authentication 
@api_view(["POST"])
@checkAccessToken
def disableTwoFactorAuth(request):
    return JsonResponse(GenericUserController.manageTwoFactorAuth(request))

#check if 2-step verification code is correct
@api_view(["POST"])
def checkTwoFactorAuthCode(request):
    return JsonResponse(GenericUserController.twoFactorAuthLogin(request))

#verify account
@api_view(["POST"])
def confirmAccount(request):
    return JsonResponse({"result": GenericUserController.confirmAccount(request)})

#send confirmation email to account
@api_view(["POST"])
def sendConfirmationEmail(request):
    return JsonResponse({"result": ConfirmationCodeController.sendConfirmationEmail(getRequestBody(request), "EmailConfirmation.html")})

#request password reset 
@api_view(["POST"])
def requestPasswordReset(request):
    return JsonResponse({"result": PasswordResetCodeController.sendPasswordResetCode(getRequestBody(request), "PasswordReset.html")})

#check if password reset code is valid
@api_view(["POST"])
def checkPasswordResetCode(request):
    return JsonResponse({"result": GenericUserController.checkPasswordResetCode(request)})

#reset password
@api_view(["POST"])
def resetPassword(request):
    return JsonResponse({"result" : GenericUserController.resetPassword(request)})

#change password
@api_view(["POST"])
@checkAccessToken
def changePassword(request):
    return JsonResponse({"result" : GenericUserController.resetPassword(request)})


#update username
@api_view(["POST"])
@checkAccessToken
def updateUsername(request):
    return JsonResponse(GenericUserController.changeUsername(request))


#delete account 
@api_view(["POST"])
@checkAccessToken
def deleteAccount(request):
    return JsonResponse(UserController.deleteAccount(request))









