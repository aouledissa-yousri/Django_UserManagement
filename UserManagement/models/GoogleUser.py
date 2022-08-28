from django.db import models
from UserManagement.models.User import User


class GoogleUser(User, models.Model):
    
    username = models.CharField(max_length = 255, default = '', unique = True)
    email = models.CharField(max_length = 255, default = '', unique = True)
   
    def setData(self, data):
        self.username = data["name"]
        self.email = data["email"]
    
    def getData(self):
        return {
            "username": self.username,
            "email": self.email,
        }