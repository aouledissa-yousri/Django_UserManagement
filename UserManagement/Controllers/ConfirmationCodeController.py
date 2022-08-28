from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.utils.html import strip_tags
from UserManagement.models import ConfirmationCode
from UserManagement.serializers import ConfirmationCodeSerializer
from django.template.loader import render_to_string
from ..models.ConfirmationCode import ConfirmationCode
from ..models.GenericUser import GenericUser
from Test.settings import EMAIL_HOST_USER
from ..extra import *
from django.utils import timezone


class ConfirmationCodeController: 
    
    @staticmethod 
    def sendConfirmationEmail(userData, template = None):
        confirmationCode = generateCode()
        message = "Hello "+ userData["username"] + ",\nThank you for signining up Here is your confirmation code: "+ confirmationCode

        code = ConfirmationCode()
        code.setData(confirmationCode, GenericUser.objects.get(username = userData["username"]))
        code = ConfirmationCodeSerializer(data = code.getData())

        if code.is_valid():
            ConfirmationCode.objects.filter(user_id = GenericUser.objects.get(username = userData["username"]).id).delete()
            print(timezone.now())
            code.save()
            if template != None:
                message = render_to_string(template, {"message": message})
                textContent = strip_tags(message)

                email = EmailMultiAlternatives("Email Confirmation", textContent, EMAIL_HOST_USER, [userData["email"]])
                email.attach_alternative(message, "text/html")
                email.send()

            else:
                EmailMessage("Email Confirmation", message, EMAIL_HOST_USER, [userData["email"]]).send()

            return "Code has been sent"

        return "Confirmation code has not been sent"

    
    
    