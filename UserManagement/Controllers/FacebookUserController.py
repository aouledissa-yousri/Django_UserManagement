from ..serializers import FacebookUserSerializer, TokenSerializer
from ..Controllers.TokenController import TokenController
from ..models import FacebookUser, Token
from django.shortcuts import redirect
from ..extra import *
import urllib.parse
import sys, json, requests


class FacebookUserController: 
    
    client_secret_data = json.loads(open(sys.path[0] + "/UserManagement/facebook_client_secret.json").read())
    authCode = ""
    userData = {}


    @staticmethod
    def facebookAuthFlow():
        
        #initialize authorization url
        authUrl = ''.join(f'''
            https://www.facebook.com/v14.0/dialog/oauth?response_type=code
            &client_id={FacebookUserController.client_secret_data["app_id"]}
            &redirect_uri={urllib.parse.quote('http://localhost:8000/manageUser/facebookLogin/')}
            &scope=public_profile&state=PyFacebook
            '''.split()
        )

        
        return {"message": authUrl}
    

    @staticmethod
    def facebookLoginGateway():
        return FacebookUserController.facebookAuthFlow()
    

    @staticmethod
    def getAuthCode(request):

        #get authorization code from authorization url
        FacebookUserController.authCode = request.build_absolute_uri().split("?")[1].split("&")[0].split("=")[1]
        return redirect("/manageUser/facebookLogin/")
    

    @staticmethod 
    def facebookLogin(request):

        #facebook login 
        if FacebookUserController.authCode == "Exchanged":

            FacebookUserController.authCode = ""

            try: 
                #search if user already exists
                FacebookUser.objects.get(profileId = FacebookUserController.userData["id"])
        
            except FacebookUser.DoesNotExist: 
                #save new facebook user
                facebookUser = FacebookUser()
                facebookUser.setData(FacebookUserController.userData)
                facebookUser = FacebookUserSerializer(data = facebookUser.getData())
                if facebookUser.is_valid():
                    facebookUser.save() 
            
            finally: 
                #getting google user data 
                facebookUser = FacebookUser.objects.get(profileId = FacebookUserController.userData["id"])

                #generating access token 
                token = Token()
                token.setData(TokenController.generateToken({
                    "username": facebookUser.username,
                    "number": random.randint(0, 10000000000000000)
                }))

                access_token = token.getData()["token"]

                #saving session token to database 
                token = TokenSerializer(data = token.getData())
                if token.is_valid():
                    token.save()

                return JsonResponse({
                    "message": "success",
                    "user": facebookUser.getData(),
                    "token": access_token
                })
            

        #get access token after exchanging it with auth code 
        elif FacebookUserController.authCode != "":
            return FacebookUserController.getAccessToken()
        
        #get authorization code
        else: 
            return FacebookUserController.getAuthCode(request)

       


    @staticmethod
    def getAccessToken():

        #prepare access token exchange url
        access_token_url = ''.join(
            f'''
            https://graph.facebook.com/v14.0/oauth/access_token?
            &redirect_uri={urllib.parse.quote('http://localhost:8000/manageUser/facebookLogin/')}
            &client_id={FacebookUserController.client_secret_data["app_id"]}
            &code={FacebookUserController.authCode} &client_secret={FacebookUserController.client_secret_data["app_secret"]}'''.split()
        )

        #request access token
        response = requests.get(access_token_url)
        response = json.loads(response.content)
        accessToken  = response['access_token']

        
        #get facebook user id 
        response = requests.get(f"https://graph.facebook.com/me?access_token={accessToken}")
        
        #get facebook user data 
        response = requests.get(f"https://graph.facebook.com/v14.0/me/?fields=name,id,email,picture&access_token={accessToken}")
        FacebookUserController.userData = json.loads(response.content)
        
        

        #delete authorization code
        FacebookUserController.authCode = "Exchanged"


        return redirect("/manageUser/facebookLogin/")

       


        
    
    
    
    


        