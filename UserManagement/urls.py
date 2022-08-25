from django.urls import path
from UserManagement import views

urlpatterns = [
    path("signUp/", views.signUp, name = "signUp"),
    path("login/", views.login),
    path("googleLoginGateway/", views.googleLoginGateway),
    path("googleLogin/", views.googleLogin),
    path("logout/", views.logout),
    path("checkTwoFactorAuthCode/", views.checkTwoFactorAuthCode),
    path("confirmAccount/", views.confirmAccount),
    path("sendConfirmationEmail/", views.sendConfirmationEmail),
    path("requestPasswordReset/", views.requestPasswordReset),
    path("checkPasswordResetCode/", views.checkPasswordResetCode),
    path("resetPassword/", views.resetPassword),
    path("changePassword/", views.changePassword),
    path("updateUsername/", views.updateUsername)

]