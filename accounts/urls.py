# accounts/urls.py
from django.urls import path

from .views import AccountCreateView, AccountDetailView

urlpatterns = [
    path("api/accounts/create/", AccountCreateView.as_view(), name="account_create"),
    path("api/accounts/<int:pk>/", AccountDetailView.as_view(), name="account_detail"),
]
