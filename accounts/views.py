from rest_framework import generics, permissions, filters

from accounts.models import Account, transaction_history
from accounts.serializers import TransactionHistorySerializer
from accounts.serializers import AccountSerializer



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

class TransactionHistoryListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = transaction_history.objects.filter(account__users=user)

        t_type = self.request.query_params.get('transaction_type')
        if t_type:
            queryset = queryset.filter(transaction_type=t_type)

        amount_min = self.request.query_params.get('amount_min')
        amount_max = self.request.query_params.get('amount_max')
        if amount_min:
            queryset = queryset.filter(amount__gte=amount_min)
        if amount_max:
            queryset = queryset.filter(amount__lte=amount_max)

        return queryset.order_by('-created_at')

class TransactionHistoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return transaction_history.objects.filter(account__users=user)