from django.db import models
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta 
from UserManagement.classes.HashModule import *
import hashlib, time, random

# Create your models here.

class User(models.Model):
    pass


class GenericUser(User, models.Model):

    username = models.CharField(max_length = 255, default = '', unique = True)
    email = models.CharField(max_length = 255, default = '', unique = True)
    password = models.CharField(max_length = 255, default = '', unique = True)
    salt = models.CharField(max_length = 255, default = '', unique = True)
    tries = models.IntegerField(default = 3)
    blocked = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    twoFactorAuth = models.BooleanField(default=False)


    def setData(self, data):
        self.username = data["username"]
        self.email = data["email"]
        self.salt = randomSalt(random.randint(1, 100))
        self.password = encryptPassword(data["password"], self.salt)
    
    def getData(self):
        return {
            "username": self.username,
            "email": self.email,
        }
    
    def getAllUserData(self): 
        data = self.getData()
        data["password"] = self.password
        data["salt"] = self.salt
        return data
    
    def getTries(self):
        return self.tries 
    
    def decrementTries(self):
        if self.tries > 0:
            self.tries -= 1 
            GenericUser.objects.filter(id = self.id).update(tries= self.getTries())
    
    def restartTries(self):
        self.tries = 3
        GenericUser.objects.filter(id = self.id).update(tries= self.getTries())
    
    def isBlocked(self):
        return self.blocked == True
    
    def block(self):
        self.blocked = True
        GenericUser.objects.filter(id = self.id).update(blocked= self.blocked)
    
    def unblock(self):
        time.sleep(10000)
        self.restartTries()
        self.blocked = False
        GenericUser.objects.filter(id = self.id).update(blocked= self.blocked)
    

    def verify(self):
        self.verified = True 
        GenericUser.objects.filter(id = self.id).update(verified= self.verified)
    
    def changePassword(self, password):
        self.salt = randomSalt(random.randint(1, 100))
        self.password = encryptPassword(password, self.salt)
        GenericUser.objects.filter(id = self.id).update(password = self.password, salt = self.salt)
    
    def updateUsername(self, username):
        self.username = username 
        GenericUser.objects.filter(id = self.id).update(username = self.username)

    @staticmethod
    def login(credentials):
        return GenericUser.objects.get( Q(username=credentials.getUsername()) | Q(email=credentials.getEmail() ))


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


class FacebookUser(User, models.Model):

    username = models.CharField(max_length = 255, default = '', unique = True)
    profileId = models.CharField(max_length = 255, default = '', unique = True)
    picture = models.CharField(max_length = 255, default = '', unique = True)

    def setData(self, data):
        self.username = data["name"]
        self.profileId = data["id"]
        self.picture = data["picture"]["data"]["url"]
    
    def getData(self):
        return {
            "username": self.username,
            "profileId": self.profileId,
            "picture": self.picture
        }
    


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
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)


    def setData(self, token, user):
        self.token = token 
        self.user = user

    def getData(self):
        return {
            "token": self.token,
            "user": self.user.id
        }


