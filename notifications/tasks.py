from celery import shared_task
from django.utils.timezone import now

from .models import Notification, Reminder
from .onesignal import OneSignalClient


@shared_task
def send_scheduled_notifications():
    """
    Sends scheduled notifications to users.
    """
    notifications = Notification.objects.filter(is_read=False, scheduled_at__lte=now())
    for notification in notifications:
        # Implement sending logic (e.g., email, push notifications, etc.)
        print(f"Sending notification to {notification.user.email}: {notification.title}")
        notification.is_read = True
        notification.save()


@shared_task
def send_reminders():
    """
    Send reminders to users if the scheduled time has arrived.
    """
    reminders = Reminder.objects.filter(is_sent=False, scheduled_at__lte=now())
    for reminder in reminders:
        # Example: Replace with actual sending logic (e.g., email, push notifications)
        print(f"Sending reminder to {reminder.user.email}: {reminder.message}")
        reminder.is_sent = True
        reminder.save()


@shared_task
def send_notification_to_users(title, message, user_ids, data=None):
    """
    Sends notifications to specific users via OneSignal.
    """
    client = OneSignalClient()
    response = client.send_notification(title, message, user_ids, data)
    print("Notification Response:", response)
