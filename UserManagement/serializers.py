from rest_framework import serializers 
from .models import * 

class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
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