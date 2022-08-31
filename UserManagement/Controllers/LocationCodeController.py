from ..extra import *
from ..serializers import LocationCodeSerializer
from Test.settings import EMAIL_HOST_USER
from ..models.GenericUser import GenericUser
from ..models.LocationCode import LocationCode
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMessage, EmailMultiAlternatives
from ..extra import generateExpirationDate


class LocationCodeController: 
    
    @staticmethod
    def sendLocationVerificationEmail(userData, request, baseUrl, template = None):
        verificationCode = generateCode()
        message = f"Hello  {userData['username']} + ,\na new location has been detected follow this link to verify it is you : {baseUrl}/?code={verificationCode}"

        code = LocationCode()
        code.setData(verificationCode, GenericUser.objects.get(username = userData["username"]), generateExpirationDate(request))
        code = LocationCodeSerializer(data = code.getData())

        if code.is_valid():
            LocationCode.objects.filter(user_id = GenericUser.objects.get(username = userData["username"]).id).delete()
            code.save()
            if template != None:
                message = render_to_string(template, {"message": message})
                textContent = strip_tags(message)

                email = EmailMultiAlternatives("New location detected", textContent, EMAIL_HOST_USER, [userData["email"]])
                email.attach_alternative(message, "text/html")
                email.send()

            else:
                EmailMessage("New location detected", message, EMAIL_HOST_USER, [userData["email"]]).send()

            return "verification link has been sent"

        return "verification link has not been sent"