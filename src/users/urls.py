from django.urls import path

from .views import UserRegisterView, UserLoginView, TokenRefreshView

urlpatterns = [
    path("user/register/", UserRegisterView.as_view(), name="user-register"),
    path("user/login/", UserLoginView.as_view(), name="user-login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
