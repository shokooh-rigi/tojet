from lessons.models import Grade, Lesson
from tojet.base_model import BaseModel
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import CustomUser


class IconTypeChoices(models.TextChoices):
    PURPOSE = 'Purpose', _('Purpose')
    STUDY_HOURS = 'StudyHours', _('Study Hours')


class FieldOfStudy(models.TextChoices):
    MATH = 'Math', _('Mathematics')
    EXPERIMENTAL = 'Experimental', _('Experimental Sciences')
    HUMANITIES = 'Humanities', _('Humanities')


class PurposeChoices(models.TextChoices):
    FINAL_EXAMS = 'Final Exams', _('Final Exams')
    ENTRANCE_EXAM = 'Entrance', _('University Entrance Exam')
    GENERAL_STUDY = 'General', _('General Study')
    EXAM_NIGHT = 'Exam Night', _('Night Before Exam')


class StudyHoursChoices(models.TextChoices):
    LESS_THAN_ONE = 'LessThan1', _('Less than 1 hour')
    ONE_TO_TWO = '1to2', _('1 to 2 hours')
    TWO_TO_FOUR = '2to4', _('2 to 4 hours')
    MORE_THAN_FOUR = 'MoreThan4', _('More than 4 hours')


class RankRangeChoices(models.TextChoices):
    RANGE_1_50 = '1-50', _('1 to 50')
    RANGE_50_100 = '50-100', _('50 to 100')
    RANGE_100_500 = '100-500', _('100 to 500')
    RANGE_500_1000 = '500-1000', _('500 to 1000')
    RANGE_1000_20000 = '1000-20000', _('1000 to 20000')
    RANGE_2000_50000 = '2000-50000', _('2000 to 50000')
    RANGE_5000_100000 = '5000-100000', _('5000 to 100000')

class Goal(BaseModel):

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="goals",
        verbose_name=_("User"),
    )
    grade = models.ForeignKey(
        Grade,
        on_delete=models.CASCADE,
        related_name="goals",
    )
    field_of_study = models.CharField(
        max_length=50,
        choices=FieldOfStudy.choices,
        default=FieldOfStudy.EXPERIMENTAL,
        verbose_name=_("Field of Study"),
    )
    purpose = models.CharField(
        max_length=50,
        choices=PurposeChoices.choices,
        default=PurposeChoices.GENERAL_STUDY,
        verbose_name=_("Purpose"),
    )
    from_rank_range = models.CharField(
        max_length=20,
        choices=RankRangeChoices.choices,
        default=RankRangeChoices.RANGE_1_50,
        verbose_name=_("From Rank Range"),
    )
    to_rank_range = models.CharField(
        max_length=20,
        choices=RankRangeChoices.choices,
        default=RankRangeChoices.RANGE_1_50,
        verbose_name=_("To Rank Range"),
    )
    study_hours = models.CharField(
        max_length=10,
        choices=StudyHoursChoices.choices,
        default=StudyHoursChoices.LESS_THAN_ONE,
        verbose_name=_("Study Hours"),
    )
    average_tenth = models.FloatField(
        verbose_name=_("Average Tenth"),
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(20)]
    )
    average_eleventh = models.FloatField(
        verbose_name=_("Average Eleventh"),
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(20)]
    )

    class Meta:
        verbose_name = _("Goal")
        verbose_name_plural = _("Goals")
        ordering = ["user", "field_of_study", "grade"]

    # Custom Validations
    def clean(self):
        from django.core.exceptions import ValidationError

        # Dynamically generate a rank mapping from choices
        rank_mapping = {choice[0]: index for index, choice in enumerate(RankRangeChoices.choices)}
        # Compare using the dynamic mapping
        if rank_mapping[self.from_rank_range] > rank_mapping[self.to_rank_range]:
            raise ValidationError(
                _("'From Rank Range' must be less than or equal to 'To Rank Range'.")
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"User: {self.user.username}, "
            f"Field: {self.get_field_of_study_display()}, "
            f"Purpose: {self.get_purpose_display()}"
        )

    def get_purpose_icon(self):
        """Fetch the purpose icon URL from the Icon model."""
        icon = Icon.objects.filter(icon_type=IconTypeChoices.PURPOSE.value, choice_value=self.purpose).first()
        return icon.icon.url if icon else None

    def get_study_hours_icon(self):
        """Fetch the study hours icon URL from the Icon model."""
        icon = Icon.objects.filter(icon_type=IconTypeChoices.STUDY_HOURS.value, choice_value=self.study_hours).first()
        return icon.icon.url if icon else None

    def get_konkoor_lessons(self):
        """
        Fetch lessons for all grades (10th, 11th, 12th) if purpose is 'Entrance'.
        """
        if self.purpose == PurposeChoices.ENTRANCE_EXAM.value:
            return Lesson.objects.filter(grade__name__in=['10th', '11th', '12th'])
        return Lesson.objects.filter(grade=self.grade)


class Icon(BaseModel):

    icon_type = models.CharField(
        max_length=20,
        choices=IconTypeChoices.choices,
        verbose_name=_("Icon Type"),
    )
    choice_value = models.CharField(
        max_length=50,
        verbose_name=_("Choice Value"),
        help_text=_("The value of the choice (e.g., 'Final Exams', '1to2', etc.)"),
    )
    icon = models.ImageField(
        upload_to="icons/",
        verbose_name=_("Icon"),
        help_text=_("Upload the icon image"),
    )

    def __str__(self):
        return f"{self.icon_type}: {self.choice_value}"
