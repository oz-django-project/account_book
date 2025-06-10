from rest_framework import generics, permissions

from accounts.models import Account
from accounts.serializers import AccountSerializer
from decimal import Decimal
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Account, TransactionHistory
from .serializers import TransactionCreateSerializer
from django.shortcuts import get_object_or_404
from .models import Account
from rest_framework.generics import CreateAPIView
from decimal import Decimal

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

class TransactionCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, account_id):
        try:
            account = Account.objects.get(id=account_id, user=request.user)
        except Account.DoesNotExist:
            return Response({"error": "계좌 못 찾겠다 다시 한번 체크 ㄱㄱ"}, status=404)

        serializer = TransactionCreateSerializer(data=request.data)
        if serializer.is_valid():
            amount = Decimal(serializer.validated_data['amount'])
            transaction_type = serializer.validated_data['transaction_type']

            if transaction_type == '입금':
                account.balance += amount
            elif transaction_type == '출금':
                if account.balance < amount:
                    return Response({"error": "니 돈 없다."}, status=400)
                account.balance -= amount
            else:
                return Response({"error": "에? 이거 안되는데??"}, status=400)

            account.save()

            TransactionHistory.objects.create(
                account=account,
                amount=amount,
                description=serializer.validated_data.get('description', ''),
                transaction_type=transaction_type,
                transfer_method='ATM',
                balance_after=Decimal(account.balance),  # ✅ 타입 확정
            )
            

            return Response({"message": f"{transaction_type} 완료", "balance": account.balance}, status=201)

        return Response(serializer.errors, status=400)
    
class TransactionCreateView(CreateAPIView):
    serializer_class = TransactionCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        account = get_object_or_404(Account, pk=self.kwargs['pk'])
        serializer.save(account=account)