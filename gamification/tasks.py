from celery import shared_task
from .models import Leaderboard


@shared_task
def update_leaderboard():
    """
    Updates the leaderboard rankings based on user points.
    """
    leaderboard_entries = Leaderboard.objects.all().order_by('-points')
    for rank, entry in enumerate(leaderboard_entries, start=1):
        entry.rank = rank
        entry.save()
    print("Leaderboard updated successfully!")
