from django.db import models

from review.enums import ReviewType
from tojet import settings
from tojet.base_model import BaseModel


class ReviewItem(BaseModel):
    """
    Represents an item (content or question) added to the review list by a user.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="review_items",
        help_text="The user who added this item to their review list."
    )
    review_type = models.CharField(
        max_length=20,
        choices=ReviewType.choices(),
        help_text="The type of item being reviewed (e.g., content, question)."
    )
    item_id = models.PositiveIntegerField(help_text="ID of the content or question being reviewed.")

    class Meta:
        unique_together = ('user', 'review_type', 'item_id')

    def __str__(self):
        return f"ReviewItem({self.user.username}, {self.review_type}, {self.item_id})"
