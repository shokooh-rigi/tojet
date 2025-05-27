from django.db import models
from django.utils import timezone

from tojet.base_manager import BaseManager


class BaseModel(models.Model):
    """
    Base model that includes created_at and updated_at fields.
    """
    created_at = models.DateTimeField( default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False, help_text="Soft delete flag.")

    objects = BaseManager()

    class Meta:
        abstract = True

    def soft_delete(self):
        """Marks the record as deleted without actually removing it from the database."""
        self.is_deleted = True
        self.save(update_fields=['is_deleted', 'updated_at'])

    def restore_object(self):
        """Restores the record from database."""

        self.is_deleted = False
        self.save(update_fields=['is_deleted', 'updated_at'])