import hashlib

class Credentials: 

    def __init__(self, data, passwordFromUser = True):
        self.username = data["username"]
        self.email = data["email"]
        
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