from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    CookieTokenObtainPairView,
    LogoutView,
    MyProfileView,
    PasswordChangeView,
    ReactiveUserView,
    RegisterView,
)

app_name = "users"

urlpatterns = [
    # API endpoints
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CookieTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", MyProfileView.as_view(), name="profile"),
    path("password/change/", PasswordChangeView.as_view(), name="password_change"),
    path("reactivate/", ReactiveUserView.as_view(), name="reactivate"),
]
