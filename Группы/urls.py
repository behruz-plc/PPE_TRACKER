from django.urls import path
from .views import notifications_view, get_notification_count

urlpatterns = [
    path("notifications/", notifications_view, name="notifications"),  # ✅ Notifications page
    path("notifications/count/", get_notification_count, name="get_notification_count"),
]
