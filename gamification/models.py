from django.db import models
from tojet import settings


class Leaderboard(models.Model):
    """
    Stores user rankings and points for the leaderboard.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="leaderboard",
        help_text="The user associated with this leaderboard entry."
    )
    points = models.PositiveIntegerField(
        default=0,
        help_text="Total points earned by the user."
    )
    rank = models.PositiveIntegerField(
        default=0,
        help_text="Current rank of the user."
    )
    last_updated = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp of the last leaderboard update."
    )

    def __str__(self):
        return f"Leaderboard({self.user.username}, Points: {self.points}, Rank: {self.rank})"
