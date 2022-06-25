import hashlib

class Credentials: 

    def __init__(self, data):
        self.username = data["username"]
        self.email = data["email"]
        self.password = hashlib.sha512(str(data["password"]).encode("UTF-8")).hexdigest()
    
    def getPassword(self):
        return self.password

    def getEmail(self):
        return self.email

    def getUsername(self):
        return self.username