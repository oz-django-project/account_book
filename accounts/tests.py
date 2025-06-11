from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from accounts.models import Account
from django.contrib.auth import get_user_model

User = get_user_model()

class AccountTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(password='1234', email='test@naver.com')
        self.client.force_authenticate(user=self.user)

    def test_dummy(self):
        self.assertEqual(1 + 1, 2)
        
def test_create_account(self):
    url = reverse('account_create')  
    data = {
        "bank_code": "001",
        "account_number": "1234567890",
        "account_type": "SAVINGS"
    }
    response = self.client.post(url, data, format='json')

    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Account.objects.count(), 1)
    self.assertEqual(Account.objects.first().account_number, "1234567890")

def test_create_transaction(self):
    url = f'/api/accounts/{self.account.pk}/transaction/'
    data = {
        "amount": 5000,
        "transaction_type": "DEPOSIT",
        "description": "입금 테스트"
    }
    response = self.client.post(url, data, format='json')

    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(self.account.transactionhistory_set.count(), 1)
    self.assertEqual(self.account.transactionhistory_set.first().amount, 5000)
