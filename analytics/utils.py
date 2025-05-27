from datetime import timedelta

from django.db import models

from analytics.models import UserActivityLog


def log_activity(
        user,
        lesson=None,
        content=None,
        activity_type='view',
        time_spent=None,
):
    """
    Logs user activity into the database.
    """
    UserActivityLog.objects.create(
        user=user,
        lesson=lesson,
        content=content,
        activity_type=activity_type,
        time_spent=time_spent
    )


def calculate_time_spent(user):
    """
    Calculates total time spent by a user across all activities.
    """
    total_time = UserActivityLog.objects.filter(user=user).aggregate(total=models.Sum('time_spent'))
    return total_time['total'] if total_time['total'] else timedelta(0)
