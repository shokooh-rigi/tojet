from django.db import models
from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters

from analytics.models import Feedback, UserActivityLog
from analytics.serializers import FeedbackSerializer, UserActivityLogSerializer
from exam_tests.models import Question
from lessons.models import UserLesson, Lesson
from review.enums import ReviewType
from review.models import ReviewItem
from analytics.enums import UserLessonStatus
from tojet import settings
from analytics.utils import calculate_time_spent


class UserAnalyticsView(APIView):
    """
    Provides detailed analytics for a specific user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        total_time_spent = calculate_time_spent(user)
        activity_logs = UserActivityLog.objects.filter(user=user).order_by('-timestamp')
        serializer = UserActivityLogSerializer(activity_logs, many=True)

        return Response({
            "total_time_spent": total_time_spent,
            "activities": serializer.data
        }, status=200)


class GlobalAnalyticsView(APIView):
    """
    Provides global insights about lessons, quizzes, and user engagement.
    """
    permission_classes = [IsAuthenticated]  # Can also restrict to admin users

    def get(self, request):
        most_popular_lesson = UserActivityLog.objects.values(
            'lesson__title'
        ).annotate(
            count=models.Count('lesson')
        ).order_by('-count').first()

        total_users = settings.AUTH_USER_MODEL.objects.count()
        total_activities = UserActivityLog.objects.count()

        return Response({
            "most_popular_lesson": most_popular_lesson,
            "total_users": total_users,
            "total_activities": total_activities
        }, status=200)


class AnalyticsView(APIView):
    """
    Provides analytics on user performance and engagement.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Accuracy in quizzes
        total_questions = Question.objects.filter(
            content__section__syllabus__lesson__user_lessons__user=user
        ).count()
        correct_answers = ReviewItem.objects.filter(
            user=user,
            review_type="question",
            is_correct=True,
        ).count()
        accuracy = (correct_answers / total_questions * 100) if total_questions > 0 else 0

        # Average time spent on lessons
        avg_time_spent = UserActivityLog.objects.filter(user=user).aggregate(
            avg_time=models.Avg("time_spent")
        )["avg_time"] or 0

        # Lessons completed per grade
        lessons_by_grade = (
            UserLesson.objects.filter(user=user, status=UserLessonStatus.COMPLETED)
            .values("lesson__grade__name")
            .annotate(count=models.Count("id"))
        )

        return Response({
            "quiz_accuracy": f"{accuracy:.2f}%",
            "average_time_spent": f"{avg_time_spent:.2f} minutes",
            "lessons_by_grade": list(lessons_by_grade),
        }, status=status.HTTP_200_OK)


class SubmitFeedbackView(APIView):
    """
    Allows users to submit feedback for a lesson.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, lesson_id):
        lesson = Lesson.objects.filter(id=lesson_id).first()
        if not lesson:
            return Response({"error": "Lesson not found."}, status=status.HTTP_404_NOT_FOUND)

        rating = request.data.get("rating")
        comments = request.data.get("comments")

        if not rating or not (1 <= int(rating) <= 5):
            return Response({"error": "Rating must be between 1 and 5."}, status=status.HTTP_400_BAD_REQUEST)

        feedback, created = Feedback.objects.get_or_create(
            user=request.user,
            lesson=lesson,
            defaults={"rating": rating, "comments": comments},
        )

        if not created:
            return Response({"message": "You have already submitted feedback for this lesson."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Feedback submitted successfully."}, status=status.HTTP_201_CREATED)


class ListFeedbackView(ListAPIView):
    """
    Lists feedback submitted by users for lessons.
    """
    permission_classes = [IsAuthenticated]
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


class RecommendationView(APIView):
    """
    Provides recommendations for lessons based on user activity and progress.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Find lessons the user hasn't started
        not_started_lessons = Lesson.objects.exclude(
            user_lessons__user=user
        )[:5]  # Limit to 5 recommendations

        # Find lessons flagged for review
        lessons_in_review = Lesson.objects.filter(
            user_lessons__user=user,
            user_lessons__status=UserLessonStatus.IN_REVIEW
        )[:5]

        # Format the response
        recommendations = [
            {
                "lesson_id": lesson.id,
                "title": lesson.title,
                "reason": "Not started yet",
            } for lesson in not_started_lessons
        ] + [
            {
                "lesson_id": lesson.id,
                "title": lesson.title,
                "reason": "Flagged for review",
            } for lesson in lessons_in_review
        ]

        return Response(recommendations, status=status.HTTP_200_OK)


class UserActivityLogFilter(filters.FilterSet):
    """
    Filters for user activity logs.
    """
    start_date = filters.DateFilter(field_name="timestamp", lookup_expr="gte")
    end_date = filters.DateFilter(field_name="timestamp", lookup_expr="lte")
    activity_type = filters.CharFilter(field_name="activity_type", lookup_expr="iexact")

    class Meta:
        model = UserActivityLog
        fields = ['activity_type', 'start_date', 'end_date']


class UserActivityLogView(ListAPIView):
    """
    Search and filter user activity logs.
    """
    serializer_class = UserActivityLogSerializer
    permission_classes = [IsAuthenticated]
    queryset = UserActivityLog.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserActivityLogFilter


class ReviewAnalyticsView(APIView):
    """
    Provides a summary of the user's review items.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        analytics = {}

        # Count items by review_type
        for review_type in ReviewType.values():
            analytics[review_type] = ReviewItem.objects.filter(user=user, review_type=review_type).count()

        # Total items in review
        total_items = sum(analytics.values())

        return Response(
            {
                "analytics": analytics,
                "total_items": total_items
            },
            status=status.HTTP_200_OK
        )
