from rest_framework import generics, permissions
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import TransactionHistory
from accounts.serializers import (
    TransactionCreateSerializer,
    TransactionHistorySerializer,
)

from .models import Account
from .serializers import AccountSerializer


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


class AccountDetailView(generics.RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]


class TransactionCreateView(CreateAPIView):
    serializer_class = TransactionCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_account(self):
        return get_object_or_404(Account, pk=self.kwargs["pk"], user=self.request.user)

    def perform_create(self, serializer):
        account = self.get_account()
        amount = serializer.validated_data["amount"]
        transaction_type = serializer.validated_data["transaction_type"]
        category = serializer.validated_data["category"]

        # 잔액 계산
        if transaction_type == "DEPOSIT":
            account.balance += amount
        elif transaction_type == "WITHDRAW":
            if account.balance < amount:
                raise serializer.ValidationError("잔액이 부족합니다.")
            account.balance -= amount

        account.save()

        serializer.save(
            account=account,
            balance_after=account.balance,
            category=category,
        )


class TransactionHistoryListView(generics.ListAPIView):
    serializer_class = TransactionHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = TransactionHistory.objects.filter(account__user=user)

        account_id = self.request.query_params.get("account")
        if account_id:
            try:
                account_id = int(account_id)
                queryset = queryset.filter(account__id=account_id, account__user=user)
            except ValueError:
                return TransactionHistory.objects.none()

        t_type = self.request.query_params.get("transaction_type")
        if t_type:
            queryset = queryset.filter(transaction_type=t_type)

        amount_min = self.request.query_params.get("amount_min")
        amount_max = self.request.query_params.get("amount_max")
        if amount_min:
            queryset = queryset.filter(amount__gte=amount_min)
        if amount_max:
            queryset = queryset.filter(amount__lte=amount_max)

        return queryset.order_by("-created_at")


class TransactionHistoryRetrieveUpdateDestroyView(
    generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = TransactionHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return TransactionHistory.objects.filter(account__user=user)
