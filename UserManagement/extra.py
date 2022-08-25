import sys
from Test.settings import SECRET_KEY
from UserManagement.models import *
from django.http import JsonResponse
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from pip._vendor import cachecontrol
import json, jwt, requests, random, secrets, string, google.auth.transport.requests


def getRequestBody(request):
    return json.loads(request.body) 


#check if access token is valid or not when making a post request to the server
def checkAccessToken(func, algorithm="HS512"):
    
    def wrapper(request, *args, **kwargs):
        try: 
            _token = request.headers["Token"]
            try:
                decodedToken = jwt.decode(_token, SECRET_KEY, algorithms = [algorithm])

                try:
                    #User.objects.get(username = decodedToken["username"])   
                    Token.objects.get(token = _token) 
                    return func(request, *args, **kwargs)
                
                except Token.DoesNotExist:
                    return JsonResponse({"response": "invalid token"})

            except jwt.exceptions.DecodeError:
                return JsonResponse({"response": "invalid token"})

        except KeyError: 
            return JsonResponse({"response": "invalid token"})

    return wrapper


#generate random confirmation/verification code
def generateCode():
    n = random.randint(6,10)
    res = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(n))
    return res


#prepare google login parameters 

def googleAuthFlow(client_secret_path):
    return Flow.from_client_secrets_file(
        client_secrets_file = client_secret_path,
        scopes=['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile', 'openid'],
        redirect_uri= 'http://127.0.0.1:8000/manageUser/googleLogin'
    )

#request google account access token 
def requestGoogleAccessToken(request):
    flow =  googleAuthFlow(sys.path[0] + "/UserManagement/client_secret.json")
    flow.fetch_token(authorization_response=request.build_absolute_uri())
    
    client_id = json.loads(open(sys.path[0] + "/UserManagement/client_secret.json").read())["web"]["client_id"]
    credentials = flow.credentials

    request_session = requests.session()    
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(cached_session)
    
    return id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=client_id
    )



