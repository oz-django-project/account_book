from datetime import date, datetime, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.timezone import make_aware

from accounts.models import Account, TransactionHistory
from analysis.analyzers import Analyzer
from analysis.models import Analysis

User = get_user_model()


class WeeklyDailyAnalysisTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="testpass"
        )
        self.account = Account.objects.create(
            user=self.user,
            account_number="1234567890",
            bank_code="001",
            account_type="CHECKING",
            balance=100000,
        )

        # 최근 7일간의 날짜
        today = date(2025, 6, 30)
        base_dates = [today - timedelta(days=i) for i in range(6, -1, -1)]

        amounts = [10000, 15000, 0, 8000, 5000, 0, 12000]
        descriptions = ["밥", "카페", "거래없음", "편의점", "간식", "거래없음", "영화"]

        for dt, amount, desc in zip(base_dates, amounts, descriptions):
            if amount > 0:
                TransactionHistory.objects.create(
                    account=self.account,
                    amount=amount,
                    transaction_type="WITHDRAW",
                    description=desc,
                    balance_after=100000 - amount,
                    created_at=make_aware(datetime.combine(dt, datetime.min.time())),
                )

    def test_analyzer_creates_analysis_instance(self):
        analyzer = Analyzer(
            user=self.user,
            about="expense",  # 'WITHDRAW' 대신 'expense'로 전달
            analysis_type="weekly",
            start_date=date(2025, 6, 24),
            end_date=date(2025, 6, 30),
        )

        result = analyzer.run()

        self.assertIsNotNone(result, "Analyzer가 None을 반환하면 안 됩니다.")
        self.assertIsInstance(
            result, Analysis, "반환값은 Analysis 인스턴스여야 합니다."
        )
        self.assertEqual(result.user, self.user)
        self.assertEqual(result.about, "expense")
        self.assertEqual(result.type, "weekly")
        self.assertTrue(result.result_image, "분석 이미지가 저장되지 않았습니다.")


class MonthlyCategoryAnalysisTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="testpass"
        )
        self.account = Account.objects.create(
            user=self.user,
            account_number="123456789",
            bank_code="001",
            account_type="CHECKING",
            balance=100000,
        )

        # 6월 거래내역 생성 (카테고리별로)
        TransactionHistory.objects.create(
            account=self.account,
            amount=10000,
            transaction_type="WITHDRAW",
            description="점심",
            balance_after=90000,
            category="식비",
            created_at=make_aware(datetime(2025, 6, 3)),
        )
        TransactionHistory.objects.create(
            account=self.account,
            amount=20000,
            transaction_type="WITHDRAW",
            description="카페",
            balance_after=70000,
            category="식비",
            created_at=make_aware(datetime(2025, 6, 10)),
        )
        TransactionHistory.objects.create(
            account=self.account,
            amount=15000,
            transaction_type="WITHDRAW",
            description="쇼핑",
            balance_after=55000,
            category="쇼핑",
            created_at=make_aware(datetime(2025, 6, 15)),
        )
        TransactionHistory.objects.create(
            account=self.account,
            amount=10000,
            transaction_type="WITHDRAW",
            description="교통비",
            balance_after=45000,
            category="교통",
            created_at=make_aware(datetime(2025, 6, 20)),
        )

    def test_monthly_category_analysis(self):
        analyzer = Analyzer(
            user=self.user,
            about="expense",
            analysis_type="monthly-category",
            start_date=date(2025, 6, 1),
            end_date=date(2025, 6, 30),
        )

        analysis = analyzer.run()

        self.assertIsNotNone(analysis)
        self.assertIsInstance(analysis, Analysis)
        self.assertEqual(analysis.user, self.user)
        self.assertEqual(analysis.about, "expense")
        self.assertEqual(analysis.type, "monthly-category")
        self.assertTrue(analysis.result_image, "분석 이미지가 저장되지 않았습니다.")
