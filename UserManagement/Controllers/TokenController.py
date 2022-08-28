from ..models import Token
from ..serializers import TokenSerializer
from django.http import JsonResponse
from Test.settings import SECRET_KEY
import jwt

class TokenController: 

    #save access token in database
    @staticmethod
    def saveToken(tk, user): 
        token = Token()
        token.setData(tk, user)
        token = TokenSerializer(data = token.getData())

        if token.is_valid():
            token.save()
    
    #delete access token from database
    @staticmethod 
    def deleteToken(tk): 
        Token.objects.filter(token = tk).delete()
    
    #generate access token
    def generateToken(payload):
        return jwt.encode(payload, SECRET_KEY, algorithm = "HS512")
    
    #decode access token 
    def decodeToken(token, algorithm = "HS512"): 
        try:
            decodedToken = jwt.decode(token, SECRET_KEY, algorithms = [algorithm])
            return decodedToken
            
        except jwt.exceptions.DecodeError:
            return {"message": "invalid token"}

