from django.urls import path
from .views import LeaderboardView, UserRankingView

urlpatterns = [
    path('gamification/leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    path('gamification/leaderboard/user-rank/', UserRankingView.as_view(), name='user-ranking'),
]
