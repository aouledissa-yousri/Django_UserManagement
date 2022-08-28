from django.urls import path
from UserManagement import views

urlpatterns = [
    path("signUp/", views.signUp, name = "signUp"),
    path("login/", views.login),
    path("googleLoginGateway/", views.googleLoginGateway),
    path("googleLogin/", views.googleLogin),
    path("facebookLoginGateway/", views.facebookLoginGateway),
    path("facebookLogin/", views.facebookLogin),
    path("logout/", views.logout),
    path("logoutAllSessions/", views.logoutAllSessions),
    path("logoutAllOtherSessions/", views.logoutAllOtherSessions),
    path("enableTwoFactorAuth/", views.enableTwoFactorAuth),
    path("disableTwoFactorAuth/", views.disableTwoFactorAuth),
    path("checkTwoFactorAuthCode/", views.checkTwoFactorAuthCode),
    path("confirmAccount/", views.confirmAccount),
    path("sendConfirmationEmail/", views.sendConfirmationEmail),
    path("requestPasswordReset/", views.requestPasswordReset),
    path("checkPasswordResetCode/", views.checkPasswordResetCode),
    path("resetPassword/", views.resetPassword),
    path("changePassword/", views.changePassword),
    path("updateUsername/", views.updateUsername),
    path("deleteAccount/", views.deleteAccount),

]