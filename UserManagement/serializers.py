from rest_framework import serializers 
from .models import * 

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
