from ..models import GenericUser
from ..extra import encryptPassword

class Credentials: 

    def __init__(self, data, passwordFromUser = True):

        self.addUsernameAndEmail(data)

        if passwordFromUser:
            self.password = encryptPassword(data["password"], GenericUser.objects.get(username = data["username"]).salt)

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
                self.username = GenericUser.objects.get(email = data["email"]).username
                print(self.username)
            elif "username" in data.keys(): 
                self.email = GenericUser.objects.get(username = data["username"]).email
            else: 
                self.username = ""
                self.email = ""
        