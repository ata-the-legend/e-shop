from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("verify/", views.UserRegisterVerifyCodeView.as_view(), name="verify_code"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("login-verify/", views.UserLoginVerifyCodeView.as_view(), name="login_verify_code"),
    path("logout/", views.UserLogoutView.as_view(), name="logout")
]