from django.db import models 
from UserManagement.models.User import User


class Token(models.Model):
    
    token = models.CharField(max_length = 255, default = '', unique = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)


    def setData(self, token, user):
        self.token = token 
        self.user = user

    def getData(self):
        return {
            "token": self.token,
            "user": self.user.id
        }