from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from UserManagement.Controllers.ConfirmationCodeController import ConfirmationCodeController
from UserManagement.Controllers.UserController import UserController
from UserManagement.Controllers.PasswordResetCodeController import PasswordResetCodeController
from UserManagement.extra import *

# Create your views here.

#user normal sign up
@api_view(["POST"])
def signUp(request):
    return JsonResponse({"signed up": UserController.signUp(request)})

#user login
@api_view(["POST"])
def login(request):
    return JsonResponse(UserController.loginGateway(request))

#google login gateway 
@api_view(["GET"])
def googleLoginGateway(request):
    return JsonResponse(UserController.googleLoginGateway())

#google login
@api_view(["GET"])
def googleLogin(request):
    return JsonResponse(UserController.googleLogin(request))

#user logout
@api_view((["post"]))
def logout(request):
    return JsonResponse(UserController.logout(request))

#check if 2-step verification code is correct
@api_view(["POST"])
def checkTwoFactorAuthCode(request):
    return JsonResponse(UserController.twoFactorAuthLogin(request))

#verify account
@api_view(["POST"])
@checkAccessToken
def confirmAccount(request):
    return JsonResponse({"result": UserController.confirmAccount(request)})

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
    return JsonResponse({"result": UserController.checkPasswordResetCode(request)})

#reset password
@api_view(["POST"])
def resetPassword(request):
    return JsonResponse({"result" : UserController.resetPassword(request)})

#change password
@api_view(["POST"])
@checkAccessToken
def changePassword(request):
    return JsonResponse({"result" : UserController.resetPassword(request)})


#update username
@api_view(["POST"])
@checkAccessToken
def updateUsername(request):
    return JsonResponse({"result" : UserController.changeUsername(request)})









