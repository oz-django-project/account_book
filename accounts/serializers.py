from rest_framework import serializers

from accounts.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "bank_code", "account_number", "account_type", "balance"]

    def create(self, validated_data):
        user = self.context["request"].user
        return Account.objects.create(user=user, **validated_data)
