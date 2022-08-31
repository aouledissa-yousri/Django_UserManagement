
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from pip._vendor import cachecontrol
from ..models.GoogleUser import GoogleUser
from ..serializers import GoogleUserSerializer
from ..Controllers.TokenController import TokenController
import google.auth.transport.requests, json, requests, sys, random

class GoogleUserController: 

    redirect_url = json.loads(open(sys.path[0] + "/UserManagement/google_client_secret.json").read())["web"]["redirect_uris"][0]

    #login using google account 
    @staticmethod 
    def googleLogin(request):

        #getting google account data using access token provided
        account_data = GoogleUserController.requestGoogleAccessToken(request)

        try: 
            #try to search if user already exists
            GoogleUser.objects.get(username = account_data["name"])

        except GoogleUser.DoesNotExist: 
            #add google account to database
            googleUser = GoogleUser()
            googleUser.setData(account_data)
            googleUser = GoogleUserSerializer(data = googleUser.getData())
            if googleUser.is_valid():
                googleUser.save()

        finally:
            #getting google user data 
            googleUser = GoogleUser.objects.get(username = account_data["name"])

            #generating access token 
            token = TokenController.generateToken({
                "username": googleUser.username,
                "id": googleUser.id,
                "number": random.randint(0, 10000000000000000)
            })

            

            #saving session token to database 
            TokenController.saveToken(token, googleUser)


            return {
                "message": "success",
                "user": googleUser.getData(),
                "token": token
            }




    #redirect to google login page 
    @staticmethod 
    def googleLoginGateway():
        flow = GoogleUserController.googleAuthFlow(sys.path[0] + "/UserManagement/google_client_secret.json")
        auth_url = flow.authorization_url()
        return {"message": auth_url}
    

    #prepare google login parameters 
    def googleAuthFlow(client_secret_path):
        return Flow.from_client_secrets_file(
            client_secrets_file = client_secret_path,
            scopes=['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile', 'openid'],
            #redirect_uri= 'http://127.0.0.1:8000/manageUser/googleLogin'
            redirect_uri = GoogleUserController.redirect_url
        )

    #request google account access token 
    def requestGoogleAccessToken(request):
        flow =  GoogleUserController.googleAuthFlow(sys.path[0] + "/UserManagement/google_client_secret.json")
        flow.fetch_token(authorization_response=request.build_absolute_uri())
    
        client_id = json.loads(open(sys.path[0] + "/UserManagement/google_client_secret.json").read())["web"]["client_id"]
        credentials = flow.credentials

        request_session = requests.session()    
        cached_session = cachecontrol.CacheControl(request_session)
        token_request = google.auth.transport.requests.Request(cached_session)
    
        return id_token.verify_oauth2_token(
            id_token=credentials._id_token,
            request=token_request,
            audience=client_id
        )