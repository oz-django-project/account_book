from django.urls import path
from accounts.views import (
    AccountCreateView,
    AccountListView,
    AccountDeleteView,
    TransactionHistoryListCreateView,
    TransactionHistoryRetrieveUpdateDestroyView,
)

urlpatterns = [
    path("accounts/create/", AccountCreateView.as_view(), name="account_create"),
    path("accounts/", AccountListView.as_view(), name="account_list"),
    path("accounts/<int:pk>/", AccountDeleteView.as_view(), name="account_delete"),
    path("transactions/", TransactionHistoryListCreateView.as_view(), name="transaction_list"),
    path("transactions/<int:pk>/", TransactionHistoryRetrieveUpdateDestroyView.as_view(), name="transaction_detail"),
]
