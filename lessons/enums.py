from enum import Enum


class UserLessonStatus(Enum):
    """
    Enum for tracking user lesson statuses with values and labels.
    """
    NOT_STARTED = ('not_started', 'Not Started')
    IN_PROGRESS = ('in_progress', 'In Progress')
    COMPLETED = ('completed', 'Completed')
    IN_REVIEW = ('in_review', 'In Review')

    def __init__(self, value, label):
        self._value_ = value
        self.label = label

    @classmethod
    def choices(cls):
        """
        Provides choices for model fields or serializers as a list of tuples.
        """
        return [(member.value, member.label) for member in cls]

    @classmethod
    def get_labels(cls):
        """
        Returns only the labels for the choices.
        """
        return [member.label for member in cls]


class SectionType(Enum):
    LEARNING = 'learning'
    QUIZ = 'quiz'

    @classmethod
    def choices(cls):
        return [(key.value, key.name.title()) for key in cls]


class ContentType(Enum):
    TEXT = 'text'
    VIDEO = 'video'
    PODCAST = 'podcast'
    QUIZ = 'quiz'

    @classmethod
    def choices(cls):
        return [(key.value, key.name.title()) for key in cls]


class ProgressType(Enum):
    """
    Enum for different progress types in the system, with human-readable labels.
    """
    LESSON = ("lesson", "Lesson")
    SYLLABUS = ("syllabus", "Syllabus")
    CONTENT = ("content", "Content")

    def __init__(self, value, label):
        self._value_ = value
        self.label = label

    @classmethod
    def choices(cls):
        """
        Provides choices for model fields or serializers.
        """
        return [(member.value, member.label) for member in cls]
