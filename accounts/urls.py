# accounts/urls.py
from django.urls import path

from .views import AccountCreateView, AccountDetailView, TransactionDetailView

urlpatterns = [
    path("accounts/create/", AccountCreateView.as_view(), name="account_create"),
    path("accounts/<int:pk>/", AccountDetailView.as_view(), name="account_detail"),
    path(
        "accounts/<int:account_pk>/transaction/<int:pk>/",
        TransactionDetailView.as_view(),
        name="transaction_detail",
    ),
]
