from ..models import Token
from ..serializers import TokenSerializer
from Test.settings import SECRET_KEY
import jwt

class TokenController: 

    @staticmethod
    def saveToken(tk, user): 
        token = Token()
        token.setData(tk, user)
        token = TokenSerializer(data = token.getData())

        if token.is_valid():
            token.save()
    
    @staticmethod 
    def deleteToken(tk): 
        Token.objects.filter(token = tk).delete()
    
    #generate access token
    def generateToken(payload):
        return jwt.encode(payload, SECRET_KEY, algorithm = "HS512")

