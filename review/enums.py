from enum import Enum


class ReviewType(Enum):
    """
    Enum for different review types in the system.
    """
    LESSON = "lesson"
    SYLLABUS = "syllabus"
    CONTENT = "content"
    QUESTION = "question"

    @classmethod
    def choices(cls):
        """
        Provides choices for model fields or serializers.
        """
        return [(key.value, key.name) for key in cls]

    @classmethod
    def values(cls):
        """
        Provides a list of all enum values.
        """
        return [key.value for key in cls]

    @classmethod
    def labels(cls):
        """
        Provides a dictionary of {value: label} for convenience.
        """
        return {choice.value: choice.name.title() for choice in cls}

