from UserManagement.models.User import User
from django.db import models

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