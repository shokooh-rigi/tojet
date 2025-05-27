from django.utils.timezone import now
from rest_framework import views, status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Lesson, Syllabus, Section, Content, UserLesson
from review.models import ReviewItem
from .serializers import LessonSerializer, SyllabusSerializer, SectionSerializer, ContentSerializer, \
    UserLessonSerializer
from .enums import UserLessonStatus, ProgressType
from tojet import settings


class CustomPagination(PageNumberPagination):
    """
    Custom pagination class for lessons.
    """
    page_size = settings.PAGE_SIZE
    page_size_query_param = 'page_size'
    max_page_size = settings.MAX_PAGE_SIZE


class ListLessonView(generics.ListAPIView):
    """
    API to retrieve a paginated list of lessons with filtering and search capabilities.
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ['grade', 'category', 'sub_category']
    search_fields = ['title', 'description']

    @swagger_auto_schema(
        operation_summary="List Lessons",
        operation_description="Retrieve a paginated list of lessons. Supports filtering by grade, category, and subcategory, and searching by title and description.",
        responses={
            200: LessonSerializer(many=True),
        },
        manual_parameters=[
            openapi.Parameter(
                "grade",
                openapi.IN_QUERY,
                description="Filter by grade ID",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "category",
                openapi.IN_QUERY,
                description="Filter by category ID",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "sub_category",
                openapi.IN_QUERY,
                description="Filter by subcategory ID",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "search",
                openapi.IN_QUERY,
                description="Search by title or description",
                type=openapi.TYPE_STRING,
            ),
        ],
    )
    def get_queryset(self):
        """
        Override to apply additional custom filters if needed.
        """
        return super().get_queryset()


class ListSyllabusView(views.APIView):
    """
    Retrieves the syllabus topics for a given lesson.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List Syllabus Topics",
        operation_description="Retrieve all syllabus topics for a specific lesson, ordered by their display order.",
        responses={
            200: SyllabusSerializer(many=True),
            404: "No syllabus found for this lesson.",
        },
        manual_parameters=[
            openapi.Parameter(
                "lesson_id",
                openapi.IN_PATH,
                description="The ID of the lesson for which syllabus topics are being retrieved.",
                type=openapi.TYPE_INTEGER,
            )
        ],
    )
    def get(self, request, lesson_id):
        syllabus = Syllabus.objects.filter(lesson_id=lesson_id).order_by('order')
        if not syllabus.exists():
            return Response({"error": "No syllabus found for this lesson."}, status=status.HTTP_404_NOT_FOUND)
        serializer = SyllabusSerializer(syllabus, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListSectionsView(views.APIView):
    """
    Retrieves sections for a specific syllabus topic.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List Sections",
        operation_description="Retrieve all sections for a specific syllabus topic, ordered by their display order.",
        responses={
            200: SectionSerializer(many=True),
        },
        manual_parameters=[
            openapi.Parameter(
                "syllabus_id",
                openapi.IN_PATH,
                description="The ID of the syllabus topic for which sections are being retrieved.",
                type=openapi.TYPE_INTEGER,
            )
        ],
    )
    def get(self, request, syllabus_id):
        sections = Section.objects.filter(syllabus_id=syllabus_id).order_by('order')
        serializer = SectionSerializer(sections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListContentView(views.APIView):
    """
    Retrieves content items within a specific section.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List Content",
        operation_description="Retrieve all content items within a specific section.",
        responses={
            200: ContentSerializer(many=True),
        },
        manual_parameters=[
            openapi.Parameter(
                "section_id",
                openapi.IN_PATH,
                description="The ID of the section for which content items are being retrieved.",
                type=openapi.TYPE_INTEGER,
            )
        ],
    )
    def get(self, request, section_id):
        content = Content.objects.filter(section_id=section_id)
        serializer = ContentSerializer(content, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TrackProgressView(views.APIView):
    """
    Handles tracking progress for a user across lessons, syllabuses, or content items.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get valid progress types and statuses",
        operation_description="Returns valid progress types (e.g., Lesson, Syllabus, Content) and statuses "
                              "(e.g., Not Started, In Progress, Completed) for tracking progress.",
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "progress_types": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "value": openapi.Schema(type=openapi.TYPE_STRING, description="Progress type value"),
                                "label": openapi.Schema(type=openapi.TYPE_STRING, description="Progress type label"),
                            },
                        ),
                        description="List of progress types",
                    ),
                    "statuses": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "value": openapi.Schema(type=openapi.TYPE_STRING, description="Status value"),
                                "label": openapi.Schema(type=openapi.TYPE_STRING, description="Status label"),
                            },
                        ),
                        description="List of status types",
                    ),
                },
            )
        }
    )
    def get(self, request):
        """
        Provides frontend with valid progress types and statuses for guidance.
        """
        progress_choices = [{"value": choice.value, "label": choice.label} for choice in ProgressType]
        status_choices = [{"value": choice.value, "label": choice.label} for choice in UserLessonStatus]
        return Response(
            {
                "progress_types": progress_choices,
                "statuses": status_choices
            },
            status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        operation_summary="Create new progress record",
        operation_description="Logs new progress for a user for a specific type (Lesson, Syllabus, or Content).",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["type", "id", "status"],
            properties={
                "type": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Progress type (e.g., Lesson, Syllabus, Content)"
                ),
                "id": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID of the resource (Lesson, Syllabus, or Content)"
                ),
                "status": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="New status (e.g., Not Started, In Progress, Completed)"
                ),
            },
        ),
        responses={
            201: "Progress created successfully",
            400: "Invalid input data",
            500: "Unhandled error occurred",
        }
    )
    def post(self, request):
        """
        Logs new progress or performs an action related to a resource.
        """
        progress_type = request.data.get('type')
        item_id = request.data.get('id')
        status_value = request.data.get('status')

        if not progress_type or not item_id or not status_value:
            return Response(
                {"error": "Missing required fields: type, id, and status."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if progress_type not in [choice.value for choice in ProgressType]:
            return Response({"error": "Invalid progress type."}, status=status.HTTP_400_BAD_REQUEST)

        if status_value not in [choice.value for choice in UserLessonStatus]:
            return Response({"error": "Invalid status value."}, status=status.HTTP_400_BAD_REQUEST)

        if progress_type == ProgressType.LESSON.value:
            return self.create_lesson_progress(request.user, item_id, status_value)
        elif progress_type == ProgressType.SYLLABUS.value:
            return self.create_syllabus_progress(request.user, item_id, status_value)
        elif progress_type == ProgressType.CONTENT.value:
            return self.create_content_progress(request.user, item_id, status_value)

        return Response({"error": "Unhandled progress type."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Update existing progress record",
        operation_description="Updates an existing progress record for a specific type (Lesson, Syllabus, or Content).",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["type", "id", "status"],
            properties={
                "type": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Progress type (e.g., Lesson, Syllabus, Content)"
                ),
                "id": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID of the resource (Lesson, Syllabus, or Content)"
                ),
                "status": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="New status (e.g., Not Started, In Progress, Completed)"
                ),
            },
        ),
        responses={
            200: "Progress updated successfully",
            400: "Invalid input data",
            404: "Progress not found",
            500: "Unhandled error occurred",
        }
    )
    def put(self, request):
        """
        Updates progress for an existing resource (idempotent operation).
        """
        progress_type = request.data.get('type')
        item_id = request.data.get('id')
        status_value = request.data.get('status')

        if not progress_type or not item_id or not status_value:
            return Response(
                {"error": "Missing required fields: type, id, and status."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if progress_type not in [choice.value for choice in ProgressType]:
            return Response({"error": "Invalid progress type."}, status=status.HTTP_400_BAD_REQUEST)

        if status_value not in [choice.value for choice in UserLessonStatus]:
            return Response({"error": "Invalid status value."}, status=status.HTTP_400_BAD_REQUEST)

        if progress_type == ProgressType.LESSON.value:
            return self.update_lesson_progress(request.user, item_id, status_value)
        elif progress_type == ProgressType.SYLLABUS.value:
            return self.update_syllabus_progress(request.user, item_id, status_value)
        elif progress_type == ProgressType.CONTENT.value:
            return self.update_content_progress(request.user, item_id, status_value)

        return Response({"error": "Unhandled progress type."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def create_lesson_progress(user, lesson_id, status_value):
        """
        Handles progress logging for a lesson.
        """
        try:
            user_lesson = UserLesson.objects.create(
                user=user,
                lesson_id=lesson_id,
                status=status_value,
                last_accessed_at=now(),
                progress_percentage=0.0
            )
            if status_value == UserLessonStatus.COMPLETED.value:
                user_lesson.progress_percentage = 100.0
            elif status_value == UserLessonStatus.IN_PROGRESS.value:
                user_lesson.progress_percentage = 50.0  # Example logic
            user_lesson.save()
            return Response({"message": f"Lesson progress created with status {status_value}."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def update_lesson_progress(user, lesson_id, status_value):
        """
        Handles progress updates for a lesson.
        """
        try:
            user_lesson = UserLesson.objects.get(
                user=user,
                lesson_id=lesson_id,
            )
            user_lesson.status = status_value
            user_lesson.last_accessed_at = now()
            if status_value == UserLessonStatus.COMPLETED.value:
                user_lesson.progress_percentage = 100.0
            elif status_value == UserLessonStatus.IN_PROGRESS.value:
                user_lesson.progress_percentage = 50.0  # Example logic
            user_lesson.save()
            return Response({"message": f"Lesson progress updated to {status_value}."}, status=status.HTTP_200_OK)
        except UserLesson.DoesNotExist:
            return Response({"error": "UserLesson not found."}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def create_syllabus_progress(user, syllabus_id, status_value):
        """
        Handles progress logging for a syllabus topic.
        """
        try:
            # Example logic to log syllabus progress
            return Response({"message": f"Syllabus progress logged as {status_value}."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def update_syllabus_progress(user, syllabus_id, status_value):
        """
        Handles progress updates for a syllabus topic.
        """
        try:
            # Example logic to update syllabus progress
            return Response({"message": f"Syllabus progress updated to {status_value}."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def create_content_progress(user, content_id, status_value):
        """
        Handles progress logging for a content item.
        """
        try:
            # Example logic to log content progress
            return Response({"message": f"Content progress logged as {status_value}."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def update_content_progress(user, content_id, status_value):
        """
        Handles progress updates for a content item.
        """
        try:
            # Example logic to update content progress
            return Response({"message": f"Content progress updated to {status_value}."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserDashboardView(views.APIView):
    """
    Provides a summary of user progress and reviews.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get User Dashboard Summary",
        operation_description="Provides a summary of the user's progress and reviews, including completed lessons, review items, overall progress percentage, and total time spent.",
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "completed_lessons": openapi.Schema(
                        type=openapi.TYPE_INTEGER,
                        description="Number of completed lessons by the user."
                    ),
                    "review_items_count": openapi.Schema(
                        type=openapi.TYPE_INTEGER,
                        description="Number of items in the user's review list."
                    ),
                    "overall_progress": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Overall progress percentage for the user (formatted as a string with two decimals)."
                    ),
                    "new_lessons": openapi.Schema(
                        type=openapi.TYPE_INTEGER,
                        description="Number of new lessons for the user that have not been started."
                    ),
                    "total_time_spend": openapi.Schema(
                        type=openapi.TYPE_INTEGER,
                        description="Total time spent by the user on all lessons, in hours."
                    ),
                },
                example={
                    "completed_lessons": 15,
                    "review_items_count": 5,
                    "overall_progress": "75.00%",
                    "new_lessons": 10,
                    "total_time_spend": 120,
                },
            ),
            401: "Unauthorized - Authentication credentials were not provided or invalid.",
        },
    )
    def get(self, request):
        user = request.user

        # Count completed lessons for the user
        completed_lessons = UserLesson.objects.filter(
            user=user,
            status=UserLessonStatus.COMPLETED.value
        ).count()

        # Count items in the user's review list
        review_items_count = ReviewItem.objects.filter(user=user).count()

        # Calculate the total lessons for the user and overall progress percentage
        total_lessons = Lesson.objects.count()  # Adjust to filter for specific user if needed
        overall_progress = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
        new_lessons = UserLesson.objects.filter(
            user=user,
            status=UserLessonStatus.NOT_STARTED.value
        ).count()
        total_time_spend = 0
        user_lessons = UserLesson.objects.filter(user=user).all()
        for user_lesson in user_lessons:
            if user_lesson.time_spend:
                total_time_spend += user_lesson.time_spend

        return Response(
            {
                "completed_lessons": completed_lessons,
                "review_items_count": review_items_count,
                "overall_progress": f"{overall_progress:.2f}%",
                "new_lessons": new_lessons,
                "total_time_spend": total_time_spend,
            },
            status=status.HTTP_200_OK,
        )

class ListUserReviewLessonsView(generics.ListAPIView):
    """
    Returns a list of all user's review lessons.
    """
    serializer_class = UserLessonSerializer
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filters the queryset to include only lessons in review status for the authenticated user.
        """
        return UserLesson.objects.filter(
            status=UserLessonStatus.IN_REVIEW.value,
            user=self.request.user
        )

    def list(self, request, *args, **kwargs):
        """
        Overrides the list method to handle cases where no lessons exist.
        """
        queryset = self.get_queryset()

        # Check if the queryset is empty
        if not queryset.exists():
            return Response(
                {"response": "No lessons are currently in review for this user."},
                status=status.HTTP_404_NOT_FOUND
            )

        # If lessons exist, proceed with the normal list behavior
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
