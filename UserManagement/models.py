from django.db import models
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta 
import hashlib
import time

# Create your models here.


class User(models.Model):

    username = models.CharField(max_length = 255, default = '', unique = True)
    email = models.CharField(max_length = 255, default = '', unique = True)
    password = models.CharField(max_length = 255, default = '', unique = True)
    tries = models.IntegerField(default = 3)
    blocked = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    twoFactorAuth = models.BooleanField(default=False)


    def setData(self, data):
        self.username = data["username"]
        self.email = data["email"]
        self.password = hashlib.sha512(str(data["password"]).encode("UTF-8")).hexdigest()
    
    def getData(self):
        return {
            "username": self.username,
            "email": self.email,
        }
    
    def getAllUserData(self): 
        data = self.getData()
        data["password"] = self.password
        return data
    
    def getTries(self):
        return self.tries 
    
    def decrementTries(self):
        if self.tries > 0:
            self.tries -= 1 
            User.objects.filter(id = self.id).update(tries= self.getTries())
    
    def restartTries(self):
        self.tries = 3
        User.objects.filter(id = self.id).update(tries= self.getTries())
    
    def isBlocked(self):
        return self.blocked == True
    
    def block(self):
        self.blocked = True
        User.objects.filter(id = self.id).update(blocked= self.blocked)
    
    def unblock(self):
        time.sleep(10000)
        print("hello")
        self.restartTries()
        self.blocked = False
        User.objects.filter(id = self.id).update(blocked= self.blocked)
    

    def verify(self):
        self.verified = True 
        User.objects.filter(id = self.id).update(verified= self.verified)
    
    def changePassword(self, password):
        self.password = hashlib.sha512(str(password).encode("UTF-8")).hexdigest() 
        User.objects.filter(id = self.id).update(password = self.password)
    
    def updateUsername(self, username):
        self.username = username 
        User.objects.filter(id = self.id).update(username = self.username)

    @staticmethod
    def login(credentials):
        return User.objects.get( Q(username=credentials.getUsername()) | Q(email=credentials.getEmail() ))



class ConfirmationCode(models.Model): 

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


class TwoFactorAuthCode(models.Model): 

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



class Token(models.Model):

    token = models.CharField(max_length = 255, default = '', unique = True)

    def setData(self, token):
        self.token = token 
    
    def getData(self):
        return {
            "token": self.token
        }


