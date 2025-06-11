from http.client import responses

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
    data = {"amount": 5000, "transaction_type": "DEPOSIT", "description": "입금 테스트"}
    response = self.client.post(url, data, format="json")

    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(self.account.transactionhistory_set.count(), 1)
    self.assertEqual(self.account.transactionhistory_set.first().amount, 5000)


class AccountTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="test@gmail.com", password="1234")
        self.client.force_authenticate(user=self.user)

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


from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import Account, TransactionHistory  # 실제 경로에 맞게 조정

User = get_user_model()


class TransactionListTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="testpassword1"
        )
        self.other_user = User.objects.create_user(
            email="test@another.com", password="anothertest1"
        )

        self.account = Account.objects.create(
            user=self.user,
            bank_code="001",
            account_number="123456",
            account_type="CHECKING",
            balance=200000,
        )
        self.other_account = Account.objects.create(
            user=self.other_user,
            bank_code="002",
            account_number="000000",
            account_type="SAVING",
            balance=10000,
        )

        TransactionHistory.objects.create(
            account=self.account,
            amount=1000,
            balance_after=201000,
            description="길바닥에서 주움",
            transaction_type="DEPOSIT",
            transfer_method="ATM",
        )
        TransactionHistory.objects.create(
            account=self.account,
            amount=2000,
            balance_after=199000,
            description="편의점",
            transaction_type="WITHDRAW",
            transfer_method="CARD",
        )
        TransactionHistory.objects.create(
            account=self.account,
            amount=3000,
            balance_after=202000,
            description="이자",
            transaction_type="DEPOSIT",
            transfer_method="INTEREST",
        )
        TransactionHistory.objects.create(
            account=self.other_account,
            amount=3000,
            balance_after=13000,
            description="갚은 돈",
            transaction_type="DEPOSIT",
            transfer_method="ATM",
        )

        self.url = reverse("transaction-list")

    def authenticate(self):
        self.client.force_authenticate(user=self.user)

    def test_list_all_transactions(self):
        self.authenticate()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_filter_by_transaction_type(self):
        self.authenticate()
        response = self.client.get(self.url, {"transaction_type": "DEPOSIT"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        for tx in response.data:
            self.assertEqual(tx["transaction_type"], "DEPOSIT")

    def test_filter_by_amount_min_max(self):
        self.authenticate()
        response = self.client.get(self.url, {"amount_min": 1500, "amount_max": 2500})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(float(response.data[0]["amount"]), 2000)

    def test_unauthenticated_user_cannot_access(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # 수정됨
