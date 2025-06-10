from rest_framework import generics, permissions

from accounts.models import Account, transaction_history
from accounts.serializers import AccountSerializer, TransactionUpdateSerializer


class AccountCreateView(generics.CreateAPIView):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]


class AccountListView(generics.ListAPIView):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)


class AccountDeleteView(generics.DestroyAPIView):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

class TransactionUpdateView(generics.UpdateAPIView):
    queryset = transaction_history.objects.all()
    serializer_class = TransactionUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(account__users=self.request.user)

class TransactionDeleteView(generics.DestroyAPIView):
    queryset = transaction_history.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(account__users=self.request.user)

