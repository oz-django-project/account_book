from rest_framework import generics, permissions, status
from rest_framework.generics import (
    CreateAPIView,
    RetrieveDestroyAPIView,
    get_object_or_404,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Account, TransactionHistory
from accounts.serializers import (
    AccountSerializer,
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


class AccountCreateView(CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AccountDetailView(RetrieveDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]


class TransactionCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        account = get_object_or_404(Account, pk=pk, user=request.user)

        serializer = TransactionCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        data = serializer.validated_data
        amount = data["amount"]
        transaction_type = data["transaction_type"]
        transfer_method = data["transfer_method"]
        description = data.get("description", "")

        if transaction_type == "DEPOSIT":
            account.balance += amount
        elif transaction_type == "WITHDRAW":
            if account.balance < amount:
                return Response(
                    {"error": "잔액이 부족합니다. 출금 금액을 확인해 주세요."},
                    status=400,
                )
            account.balance -= amount
        else:
            return Response({"error": "유효하지 않은 거래 유형입니다."}, status=400)

        account.save()

        TransactionHistory.objects.create(
            account=account,
            amount=amount,
            balance_after=account.balance,
            description=description,
            transaction_type=transaction_type,
            transfer_method=transfer_method,
        )

        return Response(
            {
                "message": f"{dict(TransactionHistory.TRANSACTION_TYPE).get(transaction_type)}이 정상적으로 처리되었습니다.",
                "balance": account.balance,
            },
            status=201,
        )


class AccountCreateView(CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class TransactionHistoryListCreateView(generics.ListCreateAPIView):
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
