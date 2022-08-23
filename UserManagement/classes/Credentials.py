import hashlib
from ..models import User

class Credentials: 

    def __init__(self, data, passwordFromUser = True):

        self.addUsernameAndEmail(data)

        if passwordFromUser:
            self.password = hashlib.sha512(str(data["password"]).encode("UTF-8")).hexdigest()

        else:
            self.password = data["password"]

        

    
    def getPassword(self):
        return self.password

    def getEmail(self):
        return self.email

    def getUsername(self):
        return self.username
    

    def addUsernameAndEmail(self, data): 
        try: 
            self.username = data["username"]
            self.email = data["email"]

        except KeyError:
            if "email" in data.keys():
                self.username = User.objects.get(email = data["email"]).username
            elif "username" in data.keys(): 
                self.email = User.objects.get(username = data["username"]).email
            else: 
                self.username = ""
                self.email = ""
        