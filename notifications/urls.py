from django.urls import path

from .views import(
ListNotificationsView,
MarkNotificationAsReadView,
DeleteNotificationView,
ReminderView,
)

urlpatterns = [
    path('notifications/', ListNotificationsView.as_view(), name='list-notifications'),
    path('notifications/mark-as-read/<int:notification_id>/', MarkNotificationAsReadView.as_view(),
         name='mark-as-read'),
    path('notifications/delete/<int:notification_id>/', DeleteNotificationView.as_view(),
         name='delete-notification'),
    path('notifications/reminders/', ReminderView.as_view(), name='reminders'),
]