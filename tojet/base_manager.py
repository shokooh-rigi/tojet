from django.db import models

class BaseManager(models.Manager):
    """
    Custom manager that ensures only non-deleted objects are returned by default.
    """

    def get_queryset(self):
        # Exclude soft-deleted records
        return super().get_queryset().filter(is_deleted=False)

    def all_with_deleted(self):
        """
        Returns all records, including soft-deleted ones.
        """
        return super().get_queryset()

    def only_deleted(self):
        """
        Returns only soft-deleted records.
        """
        return super().get_queryset().filter(is_deleted=True)
