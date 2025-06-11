from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

# Create your tests here.
from rest_framework.test import APITestCase

from accounts.models import Account, TransactionHistory

User = get_user_model()


class AccountTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(password="1234", email="test@gmail.com")
        self.client.force_authenticate(user=self.user)

    def test_dummy(self):
        self.assertEqual(1 + 1, 2)

        # 계좌 생성 테스트 !

    def test_create_account(self):
        url = reverse("account_create")
        data = {
            "bank_code": "001",
            "account_number": "1234567890",
            "account_type": "SAVINGS",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Account.objects.first().account_number, "1234567890")

    # 거래 내역 생성 테스트 !

    def test_create_transaction(self):
        url = f"/api/accounts/{self.account.pk}/transaction/"
        data = {
            "amount": 5000,
            "transaction_type": "DEPOSIT",
            "description": "입금 테스트",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.account.transactionhistory_set.count(), 1)
        self.assertEqual(self.account.transactionhistory_set.first().amount, 5000)

        # 계좌조회 테스트

    def test_retrieve_account(self):
        account = Account.objects.create(
            user=self.user,
            bank_code="001",
            account_number="1234567890",
            account_type="SAVINGS",
            balance=1000,
        )

        url = f"/api/accounts/{self.account.pk}/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["account_number"], "1234567890")
        self.assertEqual(response.data["bank_code"], "001")
        self.assertEqual(response.data["account_type"], "SAVINGS")
        self.assertEqual(str(response.data["balance"]), "1000.00")

        # 계좌 삭제 테스트 !

    def test_delete_account(self):
        account = Account.objects.create(
            user=self.user,
            bank_code="001",
            account_number="111122223333",
            account_type="CHECKING",
            balance=10000,
        )

        url = reverse("account_detail", args=[account.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Account.objects.count(), 0)

    # 거래내역 삭제 테스트
    def test_delete_transaction(self):
        account = Account.objects.create(
            user=self.user,
            bank_code="001",
            account_number="111122223333",
            account_type="CHECKING",
            balance=10000,
        )

        transaction = TransactionHistory.objects.create(
            account=account,
            amount=5000,
            transaction_type="DEPOSIT",
            description="삭제 테스트",
            balance_after="10000",
        )

        url = reverse("transaction_detail", args=[account.pk, transaction.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(account.transactions.count(), 0)

    # 거래내역 수정 테스트 코드 !
    def test_update_transaction(self):
        account = Account.objects.create(
            user=self.user,
            bank_code="001",
            account_number="111122223333",
            account_type="CHECKING",
            balance=10000,
        )

        transaction = TransactionHistory.objects.create(
            account=account,
            amount=5000,
            transaction_type="DEPOSIT",
            description="수정 전",
            balance_after=10000,
        )

        update_data = {
            "amount": 3000,
            "transaction_type": "WITHDRAW",
            "description": "수정 후",
        }

        url = reverse("transaction_detail", args=[account.pk, transaction.pk])
        response = self.client.patch(url, update_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        transaction.refresh_from_db()
        self.assertEqual(transaction.amount, 3000)
        self.assertEqual(transaction.transaction_type, "WITHDRAW")
        self.assertEqual(transaction.description, "수정 후")
