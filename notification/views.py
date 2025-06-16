from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Notification
from .serializers import NotificationSerializer


class UnreadNotificationListView(ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user, is_read=False
        ).order_by("-created_at")


class MarkNotificationAsReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk, user=request.user)
        except Notification.DoesNotExist:
            return Response(
                {"detail": "알림이 존재하지 않거나 권한이 없습니다."}, status=404
            )

        notification.is_read = True
        notification.save()
        return Response({"detail": "알림을 읽음 처리했습니다."}, status=200)
