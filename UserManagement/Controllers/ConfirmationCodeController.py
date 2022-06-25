from django.core.mail import EmailMessage
from UserManagement.models import ConfirmationCode
from UserManagement.serializers import ConfirmationCodeSerializer
from django.template.loader import render_to_string
from ..models import *
from Test.settings import EMAIL_HOST_USER
import random, secrets, string

class ConfirmationCodeController: 
    
    @staticmethod 
    def sendConfirmationEmail(userData, confirmationCode):
        message = "Hello "+ userData["username"] + ",\n Thank you for signining up Here is your confirmation code: "+ ConfirmationCodeController.generateConfirmationCode()

        code = ConfirmationCode()
        code.setData(confirmationCode, User.objects.get(username = userData["username"]))
        code = ConfirmationCodeSerializer(data = code.getData())

        if code.is_valid():
            code.save()
            EmailMessage("Email confirmation", message, EMAIL_HOST_USER, [userData["email"]]).send()
            return "Code has been sent"
        return "confirmation code was not sent"

    @staticmethod
    def sendStyledConfirmationEmail(message, email, template):
        temp = render_to_string(template, {"message": message})
        EmailMessage("Email confirmation", temp, EMAIL_HOST_USER, [email]).send()
    
    @staticmethod 
    def generateConfirmationCode():
        n = random.randint(6,10)
        res = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(n))
        return res
    