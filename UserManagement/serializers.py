from rest_framework import serializers 
from .models.GenericUser import GenericUser
from .models.GoogleUser import GoogleUser
from .models.FacebookUser import FacebookUser
from .models.ConfirmationCode import ConfirmationCode
from .models.PasswordResetCode import PasswordResetCode
from .models.TwoFactorAuthCode import TwoFactorAuthCode
from .models.Token import Token
from .models.Location import Location
from .models.LocationCode import LocationCode


class GenericUserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = GenericUser
        fields = "__all__"

class GoogleUserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = GoogleUser
        fields = "__all__"

class FacebookUserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = FacebookUser 
        fields = "__all__"

class ConfirmationCodeSerializer(serializers.ModelSerializer):
    class Meta: 
        model = ConfirmationCode
        fields = "__all__"

class PasswordResetCodeSerializer(serializers.ModelSerializer):
    class Meta: 
        model = PasswordResetCode
        fields = "__all__"

class TwoFactorAuthCodeSerializer(serializers.ModelSerializer):
    class Meta: 
        model = TwoFactorAuthCode
        fields = "__all__"

class TokenSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Token 
        fields = "__all__"

class LocationSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Location
        fields = "__all__"

class LocationCodeSerializer(serializers.ModelSerializer):
    class Meta: 
        model = LocationCode
        fields = "__all__"



