from django.test import TestCase
from django.contrib.auth import get_user_model
from analysis.models import Analysis
from .models import Notification
from datetime import date

User = get_user_model()

class NotificationSignalTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@example.com", password="testpass")

    def test_notification_created_on_analysis(self):
        # Analysis 생성
        analysis = Analysis.objects.create(
            user=self.user,
            about="expense",
            type="weekly",
            period_start=date(2025, 6, 1),
            period_end=date(2025, 6, 30),
            description="자동 분석 테스트"
        )

        # 알림이 생성되었는지 확인
        notifications = Notification.objects.filter(user=self.user)
        self.assertEqual(notifications.count(), 1)

        # 알림 메시지 확인
        notification = notifications.first()
        self.assertIn("분석 결과가 생성되었습니다", notification.message)
        self.assertFalse(notification.is_read)