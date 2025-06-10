# accounts/urls.py

from django.urls import path
from .views import TransactionCreateView
from accounts.views import TransactionCreateView


urlpatterns = [
    path('api/accounts/<int:pk>/transaction/', TransactionCreateView.as_view(), name="transaction_create"),
]
