from django.db.models.signals import post_save
from django.dispatch import receiver
from analysis.models import Analysis
from .models import Notification

@receiver(post_save, sender=Analysis)
def create_notification_on_analysis(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.user,
            message=f"{instance.period_start} ~ {instance.period_end} 분석 결과가 생성되었습니다."
        )