from rest_framework import serializers
from .models import Account
from .models import transaction_history


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "bank_code", "account_number", "account_type", "balance"]

    def create(self, validated_data):
        user = self.context["request"].user
        return Account.objects.create(user=user, **validated_data)

   #거래내역 조회
class TransactionHistorySerializer(serializers.ModelSerializer):
    account_number = serializers.CharField(source='account.account_number', read_only=True)
    user_nickname = serializers.CharField(source='account.user.nickname', read_only=True)
    class Meta:
        model = transaction_history
        fields = [
            'id', 'account_number', 'user_nickname',
            'transaction_type', 'amount', 'created_at', 'description'
        ]
