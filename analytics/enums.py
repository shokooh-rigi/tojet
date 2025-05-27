from django.db import models

class UserLessonStatus(models.TextChoices):
    NOT_STARTED = 'not_started', 'Not Started'
    IN_PROGRESS = 'in_progress', 'In Progress'
    COMPLETED = 'completed', 'Completed'
    IN_REVIEW = 'in_review', 'In Review'


class ActivityType(models.TextChoices):
    VIEW = 'view', 'View'
    QUIZ_ATTEMPT = 'quiz_attempt', 'Quiz Attempt'
    COMPLETION = 'completion', 'Completion'

