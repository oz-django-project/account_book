from django.urls import path

from .views import (
    AccountCreateView,
    AccountDeleteView,
    AccountDetailView,
    AccountListView,
    TransactionCreateView,
    TransactionHistoryListCreateView,
    TransactionHistoryRetrieveUpdateDestroyView,
)

urlpatterns = [
    path("accounts/create/", AccountCreateView.as_view(), name="account_create"),
    path("accounts/", AccountListView.as_view(), name="account_list"),
    path("accounts/<int:pk>/", AccountDetailView.as_view(), name="account_detail"),
    path(
        "accounts/<int:pk>/delete/", AccountDeleteView.as_view(), name="account_delete"
    ),
    path(
        "transactions/",
        TransactionHistoryListCreateView.as_view(),
        name="transaction_list",
    ),
    path(
        "transactions/<int:pk>/",
        TransactionHistoryRetrieveUpdateDestroyView.as_view(),
        name="transaction_detail",
    ),
    path(
        "accounts/<int:pk>/transaction/",
        TransactionCreateView.as_view(),
        name="transaction_create",
    ),
]
