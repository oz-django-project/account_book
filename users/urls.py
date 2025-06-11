from django.urls import path

from .views import (
    CookieTokenObtainPairView,
    LogoutView,
    MyProfileView,
    PasswordChangeView,
    ReactiveUserView,
    RegisterView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CookieTokenObtainPairView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", MyProfileView.as_view(), name="my_profile"),
    path("password/change/", PasswordChangeView.as_view(), name="change_password"),
    path("reactive/", ReactiveUserView.as_view(), name="reactive_user"),
]
