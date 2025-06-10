from rest_framework import serializers
from .models import Account
from .models import TransactionHistory


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "bank_code", "account_number", "account_type", "balance"]

    def create(self, validated_data):
        user = self.context["request"].user
        return Account.objects.create(user=user, **validated_data)

class TransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionHistory
        fields = [
            'id',
            'account',
            'amount',
            'description',
            'transaction_type',
            'transfer_method',
            'balance_after'
        ]
        extra_kwargs = {
            'account': {'read_only': True},
            'balance_after': {'read_only': True}
        }

   # 거래내역 조회
class TransactionHistorySerializer(serializers.ModelSerializer):
    account_number = serializers.CharField(source='account.account_number', read_only=True)
    user_nickname = serializers.CharField(source='account.user.nickname', read_only=True)
    class Meta:
        model = TransactionHistory
        fields = [
            'id', 'account_number', 'user_nickname',
            'transaction_type', 'amount', 'created_at', 'description'
        ]
        read_only_fields = ['account_number', 'user_nickname', 'created_at']
