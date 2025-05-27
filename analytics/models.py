from django.db import models
from django.core.exceptions import ValidationError

from analytics.enums import ActivityType
from tojet.base_model import BaseModel
from tojet import settings
from lessons.models import Lesson, Content


class UserActivityLog(BaseModel):
    """
    Logs user activities such as time spent on lessons and quizzes.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="activity_logs",
        help_text="The user associated with the activity."
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="activity_logs",
        help_text="The lesson associated with the activity."
    )
    content = models.ForeignKey(
        Content,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="activity_logs",
        help_text="The specific content item viewed or interacted with."
    )
    activity_type = models.CharField(
        max_length=50,
        choices=ActivityType.choices,
        help_text="The type of activity."
    )
    time_spent = models.DurationField(
        null=True,
        blank=True,
        help_text="Time spent on this activity."
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text="The timestamp of the activity."
    )

    def __str__(self):
        return f"Activity({self.user.username}, {self.get_activity_type_display()}, {self.lesson.title if self.lesson else 'N/A'})"


class Feedback(BaseModel):
    """
    Stores feedback submitted by users for lessons.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="feedback",
        help_text="The user who submitted the feedback."
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="feedback",
        help_text="The lesson the feedback is about."
    )
    rating = models.PositiveSmallIntegerField(
        help_text="Rating given by the user (1 to 5)."
    )
    comments = models.TextField(
        null=True,
        blank=True,
        help_text="Optional comments provided by the user."
    )

    def clean(self):
        if not (1 <= self.rating <= 5):
            raise ValidationError("Rating must be between 1 and 5.")

    def __str__(self):
        return f"Feedback({self.user.username}, {self.lesson.title})"


class Recommendation(BaseModel):
    """
    Stores recommendations for users based on their activity and progress.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recommendations",
        help_text="The user this recommendation is for."
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="recommended_lessons",
        help_text="The recommended lesson."
    )
    reason = models.TextField(
        help_text="Reason for this recommendation (e.g., flagged for review, high difficulty)."
    )

    def __str__(self):
        return f"Recommendation({self.user.username}, {self.lesson.title})"
