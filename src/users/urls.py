from django.urls import path

from .views import (
    UserRegisterView,
    UserLoginView,
    TokenRefreshView,
    UserListView,
    UserUpdateView,
)

urlpatterns = [
    path("user/register/", UserRegisterView.as_view(), name="user-register"),
    path("user/login/", UserLoginView.as_view(), name="user-login"),
    path("user/<int:id>/", UserUpdateView.as_view(), name="user-update"),
    path("user/all/", UserListView.as_view(), name="user-list"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
