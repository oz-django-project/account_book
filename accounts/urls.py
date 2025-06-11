from django.urls import path
from accounts.views import (
    AccountCreateView,
    AccountListView,
    AccountDeleteView,
    TransactionHistoryListCreateView,
    TransactionCreateView,
    TransactionHistoryRetrieveUpdateDestroyView,
)

from .views import AccountCreateView, AccountDetailView

urlpatterns = [
    path("accounts/create/", AccountCreateView.as_view(), name="account_create"),
    path("accounts/", AccountListView.as_view(), name="account_list"),
    path("accounts/<int:pk>/", AccountDeleteView.as_view(), name="account_delete"),
    path("transactions/", TransactionHistoryListCreateView.as_view(), name="transaction_list"),
    path("transactions/create/<int:pk>/", TransactionCreateView.as_view(), name="transaction_create"),
    path("transactions/<int:pk>/", TransactionHistoryRetrieveUpdateDestroyView.as_view(), name="transaction_detail"),
    path("create/", AccountCreateView.as_view(), name="account_create"),

    path("api/accounts/create/", AccountCreateView.as_view(), name="account_create"),
    path("api/accounts/<int:pk>/", AccountDetailView.as_view(), name="account_detail"),
]
