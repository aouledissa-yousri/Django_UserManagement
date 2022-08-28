from django.db import models 
from django.utils import timezone
from datetime import timedelta
from UserManagement.models.User import User


class PasswordResetCode(models.Model):
    
    code = models.CharField(max_length = 255, default = '', unique = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    expirationDate = models.DateTimeField(default = timezone.now() + timedelta(minutes = 5))

    def setData(self, code, user):
        self.code = code 
        self.user = user
    
    def getData(self):
        return {
            "code": self.code, 
            "user": self.user.id
        }