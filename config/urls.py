from django.contrib import admin
<<<<<<< HEAD
from django.urls import path, include
=======
from django.urls import include, path
>>>>>>> 61597038d31307e80b8187f086af280960227c59
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

<<<<<<< HEAD
=======
from accounts.views import (
    AccountCreateView,
    AccountDeleteView,
    AccountDetailView,
    AccountListView,
    TransactionCreateView,
    TransactionHistoryListCreateView,
    TransactionHistoryRetrieveUpdateDestroyView,
)
from users.views import (
    CookieTokenObtainPairView,
    LogoutView,
    MyProfileView,
    PasswordChangeView,
    ReactiveUserView,
    RegisterView,
)

>>>>>>> 61597038d31307e80b8187f086af280960227c59
schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version="v1",
        description="API description",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc-ui/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("admin/", admin.site.urls),
<<<<<<< HEAD
    path("api/users/", include("users.urls")),
    path("api/accounts/", include("accounts.urls")),
=======
    # user
    path("api/register/", RegisterView.as_view(), name="register"),
    path("api/login/", CookieTokenObtainPairView.as_view(), name="login"),
    path("api/logout/", LogoutView.as_view(), name="logout"),
    path("api/profile/", MyProfileView.as_view(), name="my_profile"),
    path("api/password/change/", PasswordChangeView.as_view(), name="change_password"),
    path("api/reactive/", ReactiveUserView.as_view(), name="reactive_user"),
    # account
    path("api/accounts/create/", AccountCreateView.as_view(), name="account_create"),
    path("api/accounts/", AccountListView.as_view(), name="account_list"),
    path("api/accounts/<int:pk>/", AccountDeleteView.as_view(), name="account_delete"),
    path("api/", include("accounts.urls")),
    path("api/accounts/<int:pk>/", AccountDetailView.as_view(), name="account_detail"),
    # transaction
    path(
        "transactions/",
        TransactionHistoryListCreateView.as_view(),
        name="transaction-list",
    ),
    path(
        "transactions/<int:pk>/",
        TransactionHistoryRetrieveUpdateDestroyView.as_view(),
        name="transaction-detail",
    ),
    path(
        "api/accounts/<int:pk>/transaction/",
        TransactionCreateView.as_view(),
        name="transaction_create",
    ),
>>>>>>> 61597038d31307e80b8187f086af280960227c59
]
