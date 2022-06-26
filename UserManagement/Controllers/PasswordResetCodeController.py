from UserManagement.extra import generateCode
from UserManagement.models import *
from django.core.mail import EmailMessage
from Test.settings import EMAIL_HOST_USER
from UserManagement.serializers import PasswordResetCodeSerializer



class PasswordResetCodeController:
    
    @staticmethod 
    def sendPasswordResetCode(userData, passwordResetCode):
        passwordResetCode = generateCode()
        message = "Hello "+ userData["username"] + ",\n Here is your password reset code : "+ passwordResetCode

        passwordReset = PasswordResetCode()
        passwordReset.setData(passwordResetCode, User.objects.get(username = userData["username"]))
        passwordReset = PasswordResetCodeSerializer(data = passwordReset.getData())

        if passwordReset.is_valid():
            PasswordResetCode.objects.filter(user_id = User.objects.get(username = userData["username"]).id).delete()
            passwordReset.save()
            EmailMessage("Password Reset", message, EMAIL_HOST_USER, [userData["email"]]).send()
            return "Passoword reset code has been sent"
        return "Password reset code was not sent"
