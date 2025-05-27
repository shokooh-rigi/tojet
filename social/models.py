from django.db import models

from tojet import settings
from tojet.base_model import BaseModel


class Post(BaseModel):
    """
    Represents a social post created by a user.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
        help_text="The user who created this post."
    )
    content = models.TextField(
        help_text="The text content of the post."
    )
    image = models.ImageField(
        upload_to=settings.POST_IMAGES_PATH,
        null=True,
        blank=True,
        help_text="Optional image for the post."
    )

    def __str__(self):
        return f"Post by {self.user.username}"


class Comment(BaseModel):
    """
    Represents a comment on a post.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
        help_text="The user who wrote this comment."
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        help_text="The post this comment belongs to."
    )
    content = models.TextField(
        help_text="The text content of the comment."
    )

    def __str__(self):
        return f"Comment by {self.user.username}"


class Like(BaseModel):
    """
    Represents a like for a post or comment.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="likes",
        help_text="The user who liked the post or comment."
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="likes",
        help_text="The post that was liked."
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="likes",
        help_text="The comment that was liked."
    )

    class Meta:
        unique_together = ('user', 'post', 'comment')

    def __str__(self):
        if self.post:
            return f"{self.user.username} liked Post {self.post.id}"
        return f"{self.user.username} liked Comment {self.comment.id}"
