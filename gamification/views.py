from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from .models import Leaderboard
from .serializers import LeaderboardSerializer


class LeaderboardView(ListAPIView):
    """
    API to retrieve the global leaderboard.
    """
    queryset = Leaderboard.objects.all().order_by('rank')
    serializer_class = LeaderboardSerializer


class UserRankingView(APIView):
    """
    API to retrieve the rank and points of the authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_leaderboard = Leaderboard.objects.filter(user=request.user).first()
        if not user_leaderboard:
            return Response(
                {"message": "User not found in leaderboard."},
                status=404
            )

        serializer = LeaderboardSerializer(user_leaderboard)
        return Response(serializer.data, status=200)
