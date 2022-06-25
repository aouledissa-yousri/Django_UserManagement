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