from django.db import models 
from .User import User


class Location(models.Model):

    ip = models.CharField(max_length = 255, default = '', unique = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)

    def setData(self, ip, user):
        self.ip = ip
        self.user = user


    def getData(self): 
        return {
            "ip": self.ip, 
            "user": self.user.id
        }