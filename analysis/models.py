from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Analysis(models.Model):
    ABOUT_CHOICES = [
        ("income", "총 수입"),
        ("expense", "총 지출"),
    ]

    TYPE_CHOICES = [
        ("weekly", "매주"),
        ("monthly-category", "월간 카테고리별"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="analysis_results"
    )
    about = models.CharField(max_length=20, choices=ABOUT_CHOICES)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    period_start = models.DateField()
    period_end = models.DateField()
    description = models.TextField()
    result_image = models.ImageField(upload_to="analysis_results/")
    summary = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.about} ({self.type}) {self.period_start} ~ {self.period_end}"
