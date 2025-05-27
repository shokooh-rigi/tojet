from gamification.models import Leaderboard


def award_points(user, points):
    """
    Adds points to the user's leaderboard entry.
    """
    leaderboard_entry, created = Leaderboard.objects.get_or_create(user=user)
    leaderboard_entry.points += points
    leaderboard_entry.save()
    return leaderboard_entry
