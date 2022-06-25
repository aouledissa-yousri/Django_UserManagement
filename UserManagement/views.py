from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from UserManagement.Controllers.ConfirmationCodeController import ConfirmationCodeController
from UserManagement.Controllers.UserController import UserController
from UserManagement.extra import *

# Create your views here.

#user normal sign up
@api_view(["POST"])
def signUp(request):
    return JsonResponse({"signed up": UserController.signUp(request)})

@api_view(["POST"])
def login(request):
    return JsonResponse( UserController.login(request))

@api_view(["POST"])
def confirmAccount(request):
    return JsonResponse({"result": UserController.confirmAccount(request)})

@api_view(["POST"])
@checkAccessToken
def sendConfirmationEmail(request):
    return JsonResponse({"result": ConfirmationCodeController.sendConfirmationEmail(getRequestBody(request), ConfirmationCodeController.generateConfirmationCode())})






