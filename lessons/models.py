from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.apps import apps

from tojet import settings
from tojet.base_model import BaseModel
from tojet.base_model import BaseModel
from . import apps
from .enums import UserLessonStatus, SectionType, ContentType


class Grade(BaseModel):
    """
    Represents an academic grade level for lessons, such as 10th, 11th, or 12th.
    """
    name = models.CharField(
        max_length=50,
        unique=True,
        help_text="The name of the grade."
    )

    def __str__(self):
        return self.name


class Category(BaseModel):
    """
    Represents the main category for lessons, such as Science, Arts, or Mathematics مقطع یعنی؟؟.
    """
    # todo : رشته یعنی؟
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="The name of the category."
    )

    def __str__(self):
        return self.name


class SubCategory(BaseModel):
    """
    Represents a subcategory within a category, such as Physics or Chemistry under Science. (عمومی-کنکور-نهایی)
    """
    # todo: whats different between ((عمومی-کنکور-نهایی))it and  PurposeChoices???
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="The name of the subcategory."
    )

    def __str__(self):
        return self.name


class Lesson(BaseModel):
    """
    Represents a lesson, which belongs to a grade, category, and subcategory.
    Each lesson contains basic details like title and description.تاریخ دهم
    """
    title = models.CharField(
        max_length=255,
        default="Default Title",
        help_text="The title of the lesson."
    )
    description = models.TextField(
        default="Default description",
        help_text="A description of the lesson."
    )
    grade = models.ForeignKey(
        'lessons.Grade',
        on_delete=models.CASCADE,
        related_name="lessons",
        null=True,
        blank=True,
        help_text="The academic grade this lesson belongs to."
    )
    category = models.ForeignKey(
        'lessons.Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lessons",
        help_text="The main category of this lesson."
    )
    sub_category = models.ForeignKey(
        'lessons.SubCategory',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lessons",
        help_text="The subcategory this lesson falls under."
    )

    def __str__(self):
        return self.title


class Section(BaseModel):
    """
    Represents a section within a syllabus topic, such as a learning or quiz section.
    """
    syllabus = models.ForeignKey(
        'lessons.Syllabus',
        on_delete=models.CASCADE,
        related_name="sections",
        help_text="The syllabus topic this section belongs to."
    )
    name = models.CharField(
        max_length=100,
        help_text="The name of the section (e.g., Learning, Quiz)."
    )
    type = models.CharField(
        max_length=50,
        choices=SectionType.choices(),
        help_text="The type of the section, such as learning material or quiz."
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Ordering within the syllabus."
    )

    def __str__(self):
        return f"{self.syllabus.title} - {self.name}"


class Content(BaseModel):
    """
    Represents a specific content item within a section, such as a text, video, podcast, or quiz.
    """
    section = models.ForeignKey(
        'lessons.Section',
        on_delete=models.CASCADE,
        related_name="contents",
        help_text="The section this content belongs to."
    )
    name = models.CharField(
        max_length=255,
        help_text="The name of the content."
    )
    content_type = models.CharField(
        max_length=50,
        choices=ContentType.choices(),
        help_text="The type of content (e.g., Text, Video, Podcast, Quiz)."
    )
    content_url = models.URLField(
        null=True,
        blank=True,
        help_text="URL for video or podcast content, if applicable."
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text="Additional details about the content."
    )

    def __str__(self):
        return f"{self.section.name} - {self.name}"

    def clean(self):
        if self.content_type in [ContentType.VIDEO.value, ContentType.PODCAST.value] and not self.content_url:
            raise ValidationError(f"Content URL is required for {self.content_type} content.")
        super().clean()


class Syllabus(BaseModel):
    """
    Represents a syllabus topic within a lesson.
    Each syllabus has a title and an order for arranging it within a lesson.
    """
    lesson = models.ForeignKey(
        'lessons.Lesson',
        on_delete=models.CASCADE,
        related_name="syllabus",
        help_text="The lesson this syllabus belongs to."
    )
    title = models.CharField(
        max_length=255,
        help_text="The title of the syllabus topic."
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Ordering of the syllabus within the lesson."
    )
    stars = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="The number of stars this syllabus belongs to."
    )
    estimate_study_time = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="The estimated time this syllabus belongs to."
    )

    def __str__(self):
        return f"{self.lesson.title} - {self.title}"

    def clean(self):
        if self.stars < 1 or self.stars > 5:
            raise ValidationError("Stars must be between 1 and 5.")
        if self.estimate_study_time < 0:
            raise ValidationError("Estimated study time cannot be negative.")


class UserLesson(BaseModel):
    """
    Tracks a user's interaction with a specific lesson, including progress and review status.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_lessons",
        help_text="The user associated with this lesson interaction."
    )
    lesson = models.ForeignKey(
        'lessons.Lesson',
        on_delete=models.CASCADE,
        related_name="user_lessons",
        help_text="The lesson being tracked."
    )
    status = models.CharField(
        max_length=50,
        choices=UserLessonStatus.choices(),
        default=UserLessonStatus.NOT_STARTED.value,
        help_text="The status of the user's progress in the lesson."
    )
    progress_percentage = models.FloatField(
        default=0.0,
        help_text="The percentage of the lesson completed by the user."
    )
    last_accessed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="The last time the user accessed this lesson."
    )
    time_spend = models.FloatField(
        null=True,
        blank=True,
        help_text="The amount of time that user spent in the lesson."
    )
    accuracy_percentage = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text="User's accuracy percentage for responses in this lesson."
    )
    points_earned = models.PositiveIntegerField(
        default=0,
        help_text="The amount of points earned in this lesson."
    )

    class Meta:
        unique_together = ('user', 'lesson')
        verbose_name = "User Lesson"
        verbose_name_plural = "User Lessons"

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title} ({self.status})"

    def mark_completed(self):
        """
        Marks the lesson as completed and sets progress to 100%.
        """
        self.status = UserLessonStatus.COMPLETED.value
        self.progress_percentage = 100.0
        self.save()

    def mark_in_progress(self):
        """
        Marks the lesson as in progress if not already completed.
        """
        if self.status != UserLessonStatus.COMPLETED.value:
            self.status = UserLessonStatus.IN_PROGRESS.value
            self.save()

    def calculate_lesson_accuracy(self):
        """
        Calculates the accuracy of the user's progress in this lesson.
        """
        # Lazily resolve models to avoid circular imports
        Content = apps.get_model('lessons', 'Content')
        Question = apps.get_model('exam_tests', 'Question')
        UserAnswer = apps.get_model('exam_tests', 'UserAnswer')

        quiz_contents = Content.objects.filter(
            section__syllabus__lesson=self.lesson,
            content_type=ContentType.QUIZ.value,
        )

        total_questions = Question.objects.filter(content__in=quiz_contents).count()
        correct_answers = UserAnswer.objects.filter(
            user=self.user,
            question__content__in=quiz_contents,
            is_correct=True,
        ).count()

        accuracy = (correct_answers / total_questions * 100) if total_questions > 0 else 0
        return accuracy