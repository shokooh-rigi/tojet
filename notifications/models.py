from django.db import models
from django.utils.timezone import now
from tojet.base_model import BaseModel
from tojet import settings


class NotificationType(models.TextChoices):
    """
    Defines readable choices for notification types.
    """
    REMINDER = 'reminder', 'Reminder'
    UPDATE = 'update', 'Update'
    SOCIAL = 'social', 'Social Interaction'


class Notification(BaseModel):
    """
    Stores notifications for users related to reminders, updates, etc.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
        help_text="The user who will receive the notification."
    )
    title = models.CharField(
        max_length=255,
        help_text="Title of the notification."
    )
    message = models.TextField(
        help_text="The content of the notification."
    )
    is_read = models.BooleanField(
        default=False,
        help_text="Whether the notification has been read by the user."
    )
    scheduled_at = models.DateTimeField(
        default=now,
        help_text="When the notification was scheduled to be sent."
    )
    notification_type = models.CharField(
        max_length=50,
        choices=NotificationType.choices,
        help_text="Type of notification."
    )

    def __str__(self):
        return f"Notification for {self.user.username}: {self.title}"


class Reminder(BaseModel):
    """
    Stores reminders for users.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reminders",
        help_text="The user this reminder is for."
    )
    message = models.TextField(
        help_text="Reminder message for the user."
    )
    scheduled_at = models.DateTimeField(
        help_text="When the reminder should be sent."
    )
    is_sent = models.BooleanField(
        default=False,
        help_text="Whether the reminder has been sent."
    )

    def __str__(self):
        return f"Reminder for {self.user.username} at {self.scheduled_at}"
