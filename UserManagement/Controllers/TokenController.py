from ..models import Token
from ..serializers import TokenSerializer

class TokenController: 

    @staticmethod
    def saveToken(tk): 
        token = Token()
        token.setData(tk)
        token = TokenSerializer(data = token.getData())
        print(token)

        if token.is_valid():
            token.save()
    
    @staticmethod 
    def deleteToken(tk): 
        Token.objects.filter(token = tk).delete()
