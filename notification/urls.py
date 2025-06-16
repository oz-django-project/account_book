from django.urls import path

from .views import MarkNotificationAsReadView, UnreadNotificationListView

urlpatterns = [
    path(
        "notifications/unread/",
        UnreadNotificationListView.as_view(),
        name="unread-notification-list",
    ),
    path(
        "notifications/<int:pk>/read/",
        MarkNotificationAsReadView.as_view(),
        name="mark-notification-as-read",
    ),
]
