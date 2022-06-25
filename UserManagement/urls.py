from django.urls import path
from UserManagement import views

urlpatterns = [
    path("signUp/", views.signUp, name = "signUp"),
    path("login/", views.login),
    path("confirmAccount/", views.confirmAccount),
    path("sendConfirmationEmail/", views.sendConfirmationEmail)

]