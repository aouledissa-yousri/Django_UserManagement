from django.db import models 
from UserManagement.models.User import User
from datetime import datetime
from datetime import timedelta


class TwoFactorAuthCode(models.Model): 

    code = models.CharField(max_length = 255, default = '', unique = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    expirationDate = models.DateTimeField(default = datetime.now() + timedelta(minutes = 5))

    def setData(self, code, user, expirationDate):
        self.code = code 
        self.user = user
        self.expirationDate = expirationDate
    
    def getData(self):
        return {
            "code": self.code, 
            "user": self.user.id
        }