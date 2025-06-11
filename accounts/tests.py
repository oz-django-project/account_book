from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

# Create your tests here.
from rest_framework.test import APITestCase

from accounts.models import Account

User = get_user_model()


class AccountTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(password="1234", email="test@gmail.com")
        self.client.force_authenticate(user=self.user)

    def test_dummy(self):
        self.assertEqual(1 + 1, 2)


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

    def test_create_account(self):
        url = reverse("account_create")
        data = {
            "bank_code": "001",
            "account_number": "1234567890",
            "account_type": "SAVING",
            "balance": 0,
        }

        response = self.client.post(url, data, format="json")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Account.objects.first().account_number, "1234567890")

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
