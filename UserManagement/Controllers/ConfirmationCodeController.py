from django.core.mail import EmailMessage
from UserManagement.models import ConfirmationCode
from UserManagement.serializers import ConfirmationCodeSerializer
from django.template.loader import render_to_string
from ..models import *
from Test.settings import EMAIL_HOST_USER
from ..extra import *

class ConfirmationCodeController: 
    
    @staticmethod 
    def sendConfirmationEmail(userData, confirmationCode):
        message = "Hello "+ userData["username"] + ",\n Thank you for signining up Here is your confirmation code: "+ generateCode()

        code = ConfirmationCode()
        code.setData(confirmationCode, User.objects.get(username = userData["username"]))
        code = ConfirmationCodeSerializer(data = code.getData())

        if code.is_valid():
            ConfirmationCode.objects.filter(user_id = User.objects.get(username = userData["username"]).id).delete()
            code.save()
            EmailMessage("Email confirmation", message, EMAIL_HOST_USER, [userData["email"]]).send()
            return "Code has been sent"
        return "confirmation code was not sent"

    @staticmethod
    def sendStyledConfirmationEmail(message, email, template):
        temp = render_to_string(template, {"message": message})
        EmailMessage("Email confirmation", temp, EMAIL_HOST_USER, [email]).send()
    
    
    