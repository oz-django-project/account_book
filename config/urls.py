from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

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
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"
    ),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    # admin
    path("admin/", admin.site.urls),
    path("api/", include("users.urls")),
    path("api/", include("accounts.urls")),
]
