from django.urls import path

from .views import RegisterUser, LoginUser, LogoutUser, GetEditUser, PasswordChangeView

urlpatterns = [
    path("register/", RegisterUser.as_view(), name="register"),
    path("login/", LoginUser.as_view(), name="login"),
    path("logout/", LogoutUser.as_view(), name="logout"),
    path("", GetEditUser.as_view(), name="get_edit_user"),
    path("password_change/", PasswordChangeView.as_view(), name="password_change"),
]
