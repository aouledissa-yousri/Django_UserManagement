from UserManagement.models.User import User
from django.db import models
from ..classes.HashModule import *
from django.db.models import Q
from ..extra import *
import hashlib, time, random





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


