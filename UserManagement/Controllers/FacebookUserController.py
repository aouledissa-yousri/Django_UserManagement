from pyfacebook import GraphAPI
from ..extra import *
from django.shortcuts import redirect
import urllib.parse
import sys, json, requests


class FacebookUserController: 
    
    client_secret_data = json.loads(open(sys.path[0] + "/UserManagement/facebook_client_secret.json").read())
    authCode = ""


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
            
            return JsonResponse({"message": "logged in"})

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
        print(response)


        #delete authorization code
        FacebookUserController.authCode = "Exchanged"


        return redirect("/manageUser/facebookLogin")

       


        
    
    
    
    


        