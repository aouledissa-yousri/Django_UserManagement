from UserManagement.extra import generateCode
from UserManagement.models.TwoFactorAuthCode import TwoFactorAuthCode
from UserManagement.models.User import User
from UserManagement.serializers import *
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives, EmailMessage
from Test.settings import EMAIL_HOST_USER


class TwoFactorAuthCodeController: 


    #send two factor authentication code to the user's email address
    @staticmethod 
    def sendTwoFactorAuthCode(userData, template=None):
        twoFactorAuthCode = generateCode()
        message = "Hello "+ userData["username"] + ",\nHere is your 2-step verification code : "+ twoFactorAuthCode

        twoFactorCode = TwoFactorAuthCode()
        twoFactorCode.setData(twoFactorAuthCode, User.objects.get(username = userData["username"]))
        twoFactorCode = TwoFactorAuthCodeSerializer(data = twoFactorCode.getData())

        if twoFactorCode.is_valid():
            TwoFactorAuthCode.objects.filter(user_id = User.objects.get(username = userData["username"]).id).delete()
            twoFactorCode.save()
            if template != None:
                message = render_to_string(template, {"message": message})
                textContent = strip_tags(message)

                email = EmailMultiAlternatives("2-Step verification code", textContent, EMAIL_HOST_USER, [userData["email"]])
                email.attach_alternative(message, "text/html")
                email.send()

            else:
                EmailMessage("2-Step verification code", message, EMAIL_HOST_USER, [userData["email"]]).send()
                
            return "Verification code has been sent to your email address"

        return "Verification code has not been sent"
