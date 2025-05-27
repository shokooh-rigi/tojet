from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from exam_tests.models import Question, UserAnswer, Exam
from exam_tests.serializers import QuestionSerializer, UserAnswerSerializer, ExamSerializer


class UserStatsView(views.APIView):
    """
    Provides statistics about a user's performance.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get User Statistics",
        operation_description="Retrieve total answers, correct answers, and average time per question for the authenticated user.",
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "total_answers": openapi.Schema(type=openapi.TYPE_INTEGER, description="Total answers submitted by the user."),
                    "correct_answers": openapi.Schema(type=openapi.TYPE_INTEGER, description="Number of correct answers."),
                    "average_time": openapi.Schema(type=openapi.TYPE_NUMBER, description="Average time (in seconds) spent per question."),
                },
            ),
            401: "Unauthorized access.",
        },
    )
    def get(self, request):
        user = request.user
        total_answers = UserAnswer.objects.filter(user=user).count()
        correct_answers = UserAnswer.objects.filter(user=user, is_correct=True).count()
        average_time = UserAnswer.objects.filter(user=user).aggregate(models.Avg('time_taken'))['time_taken__avg']

        return Response({
            "total_answers": total_answers,
            "correct_answers": correct_answers,
            "average_time": average_time or 0,
        }, status=status.HTTP_200_OK)


class ListQuestionsView(views.APIView):
    """
    Retrieves questions for a specific content item.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List Questions",
        operation_description="Fetch all questions associated with a specific content item by providing its ID.",
        responses={
            200: QuestionSerializer(many=True),
            404: "Content with the given ID does not contain any questions.",
        },
    )
    def get(self, request, content_id):
        questions = Question.objects.filter(content_id=content_id)
        if not questions.exists():
            return Response({"message": "No questions found for this content."}, status=status.HTTP_404_NOT_FOUND)

        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubmitAnswerView(views.APIView):
    """
    Submits an answer for a specific question and evaluates its correctness.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Submit Answer",
        operation_description="Submit an answer to a question. Provide the question ID, selected answer, and the time taken.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["question_id", "selected_answer", "time_taken"],
            properties={
                "question_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the question."),
                "selected_answer": openapi.Schema(type=openapi.TYPE_STRING, description="The user's selected answer."),
                "time_taken": openapi.Schema(type=openapi.TYPE_INTEGER, description="Time taken by the user to answer, in seconds."),
            },
        ),
        responses={
            201: UserAnswerSerializer,
            400: "Invalid data or missing fields.",
            404: "Question not found.",
        },
    )
    def post(self, request):
        question_id = request.data.get('question_id')
        selected_answer = request.data.get('selected_answer')
        time_taken = request.data.get('time_taken')

        if not question_id or not selected_answer or time_taken is None:
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

        question = get_object_or_404(Question, id=question_id)
        user_answer = UserAnswer.objects.create(
            user=request.user,
            question=question,
            selected_option=selected_answer,
            time_taken=time_taken
        )

        serializer = UserAnswerSerializer(user_answer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ListExamsView(views.APIView):
    """
    Retrieves a list of all available exams.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List Exams",
        operation_description="Fetch all available exams in the system.",
        responses={
            200: ExamSerializer(many=True),
            401: "Unauthorized access.",
        },
    )
    def get(self, request):
        exams = Exam.objects.all()
        serializer = ExamSerializer(exams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
