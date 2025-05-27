from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from users.services.sms_provider.sms_provider_factory import logger
from .models import Goal
from .serializers import GoalSerializer, GoalChoicesSerializer


def health_check(request):
    return JsonResponse({"status": "ok"})


class GoalChoicesView(APIView):
    """
    API endpoint to retrieve goal-related choices such as fields of study, purposes, study hours, and rank ranges.
    """
    @swagger_auto_schema(
        operation_summary="Get Goal Choices",
        operation_description="Retrieve all choices for goals, including field of study, purpose, study hours, and rank ranges.",
        responses={200: openapi.Schema(type=openapi.TYPE_OBJECT)}
    )
    def get(self, request, *args, **kwargs):
        serializer = GoalChoicesSerializer()
        return Response(serializer.to_representation(None))

class CreateGoalView(CreateAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

class ListGoalView(ListAPIView):
    queryset = Goal.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = GoalSerializer


class UpdateGoalView(UpdateAPIView):
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return goals belonging to the authenticated user
        return Goal.objects.filter(user=self.request.user)
