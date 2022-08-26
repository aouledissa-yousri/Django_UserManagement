from django.shortcuts import render
from django.http import JsonResponse
from UserManagement.Controllers.GoogleUserController import GoogleUserController
from rest_framework.decorators import api_view
from UserManagement.Controllers.ConfirmationCodeController import ConfirmationCodeController
from UserManagement.Controllers.GenericUserController import GenericUserController
from UserManagement.Controllers.PasswordResetCodeController import PasswordResetCodeController
from UserManagement.extra import *

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

#user logout
@api_view((["post"]))
def logout(request):
    return JsonResponse(GenericUserController.logout(request))

#check if 2-step verification code is correct
@api_view(["POST"])
def checkTwoFactorAuthCode(request):
    return JsonResponse(GenericUserController.twoFactorAuthLogin(request))

#verify account
@api_view(["POST"])
@checkAccessToken
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
    return JsonResponse({"result" : GenericUserController.changeUsername(request)})









