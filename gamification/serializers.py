from rest_framework import serializers
from .models import Leaderboard


class LeaderboardSerializer(serializers.ModelSerializer):
    """
    Serializer for leaderboard entries.
    """
    user = serializers.StringRelatedField()  # Display username instead of ID

    class Meta:
        model = Leaderboard
        fields = ['rank', 'user', 'points', 'last_updated']
