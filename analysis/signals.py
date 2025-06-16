from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Analysis
from .tasks import generate_ai_summary_for_analysis

@receiver(post_save, sender=Analysis)
def trigger_summary_generation(sender, instance, created, **kwargs):
    if created:
        generate_ai_summary_for_analysis.delay(instance.id)