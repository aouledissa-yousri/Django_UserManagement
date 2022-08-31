from UserManagement.extra import generateCode
from UserManagement.models.User import User
from UserManagement.models.PasswordResetCode import PasswordResetCode
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from Test.settings import EMAIL_HOST_USER
from UserManagement.serializers import PasswordResetCodeSerializer
from ..extra import generateExpirationDate



class PasswordResetCodeController:
    
    #send password reset code to the user's email address
    @staticmethod 
    def sendPasswordResetCode(userData, request, template = None):
        passwordResetCode = generateCode()
        message = "Hello "+ userData["username"] + ",\n Here is your password reset code : "+ passwordResetCode

        passwordReset = PasswordResetCode()
        passwordReset.setData(passwordResetCode, User.objects.get(username = userData["username"]), generateExpirationDate(request))
        passwordReset = PasswordResetCodeSerializer(data = passwordReset.getData())

        if passwordReset.is_valid():
            PasswordResetCode.objects.filter(user_id = User.objects.get(username = userData["username"]).id).delete()
            passwordReset.save()
            if template != None:
                message = render_to_string(template, {"message": message})
                textContent = strip_tags(message)

                email = EmailMultiAlternatives("Password Reset Code", textContent, EMAIL_HOST_USER, [userData["email"]])
                email.attach_alternative(message, "text/html")
                email.send()

            else:
                EmailMessage("Password Reset Code", message, EMAIL_HOST_USER, [userData["email"]]).send()
                
            return "Passoword reset code has been sent"

        return "Password reset code has not been sent"