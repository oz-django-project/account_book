from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{'읽음' if self.is_read else '읽지 않음'}] {self.message[:30]}"