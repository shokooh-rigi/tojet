from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import views, status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from exam_tests.models import Question
from lessons.models import Content, Lesson, Syllabus
from lessons.views import CustomPagination
from review.models import ReviewItem
from review.serializers import ReviewItemSerializer


class AddReviewItemView(views.APIView):
    """
    Adds multiple items (content, question, lesson, or syllabus) to the user's review list.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Add items to review list",
        operation_description="Add multiple items (content, question, lesson, syllabus) to the user's review list.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'review_type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="The type of item to add (e.g., content, question, lesson, syllabus)"
                ),
                'item_ids': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                    description="List of item IDs to add to the review list."
                ),
            },
            required=['review_type', 'item_ids']
        ),
        responses={
            201: openapi.Response(
                description="Items added successfully",
                examples={
                    "application/json": {
                        "message": "Added 3 items to the review list.",
                        "created_items": [1, 2, 3]
                    }
                },
            ),
            400: "Invalid input or missing parameters."
        }
    )
    def post(self, request):
        review_type = request.data.get('review_type')  # "content" or "question"
        item_ids = request.data.get('item_ids', [])

        if not review_type or not item_ids:
            return Response(
                {"error": "review_type and item_ids are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        created_items = []
        for item_id in item_ids:
            # Validate the item existence based on type
            if review_type == 'content' and not Content.objects.filter(id=item_id).exists():
                continue
            if review_type == 'question' and not Question.objects.filter(id=item_id).exists():
                continue
            if review_type == 'lesson' and not Lesson.objects.filter(id=item_id).exists():
                continue
            if review_type == 'syllabus' and not Syllabus.objects.filter(id=item_id).exists():
                continue

            # Create or fetch the review item
            _, created = ReviewItem.objects.get_or_create(
                user=request.user,
                review_type=review_type,
                item_id=item_id
            )
            if created:
                created_items.append(item_id)

        return Response(
            {"message": f"Added {len(created_items)} items to the review list.", "created_items": created_items},
            status=status.HTTP_201_CREATED
        )


class ListReviewItemsView(ListAPIView):
    """
    Lists all review items for the authenticated user with pagination.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewItemSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['review_type']  # Add more filters if needed
    search_fields = ['item_id']  # Search by item_id or related metadata

    @swagger_auto_schema(
        operation_summary="List review items",
        operation_description="Retrieve all review items for the authenticated user with filtering and pagination.",
        responses={
            200: openapi.Response(
                description="List of review items",
                schema=ReviewItemSerializer(many=True)
            )
        }
    )
    def get(self, request, *args, **kwargs):
        """
        This method is inherited from ListAPIView and documented using @swagger_auto_schema.
        """
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        """
        Filters the queryset to include only items for the authenticated user.
        """
        return ReviewItem.objects.filter(user=self.request.user)


class RemoveReviewItemView(views.APIView):
    """
    Removes multiple items from the user's review list.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Remove items from review list",
        operation_description="Remove multiple items (content, question, lesson, syllabus) from the user's review list.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'review_type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="The type of item to remove (e.g., content, question, lesson, syllabus)"
                ),
                'item_ids': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                    description="List of item IDs to remove from the review list."
                ),
            },
            required=['review_type', 'item_ids']
        ),
        responses={
            200: openapi.Response(
                description="Items removed successfully",
                examples={
                    "application/json": {
                        "message": "Removed 3 items from the review list.",
                        "removed_items": [1, 2, 3]
                    }
                },
            ),
            400: "Invalid input or missing parameters.",
            404: "Item not found in the review list."
        }
    )
    def delete(self, request):
        review_type = request.data.get('review_type')  # content or question
        item_ids = request.data.get('item_ids', [])

        if not review_type or not item_ids:
            return Response(
                {"error": "review_type and item_ids are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        removed_items = []
        for item_id in item_ids:
            try:
                review_item = ReviewItem.objects.get(
                    user=request.user,
                    review_type=review_type,
                    item_id=item_id
                )
                review_item.delete()
                removed_items.append(item_id)
            except ReviewItem.DoesNotExist:
                continue

        return Response(
            {"message": f"Removed {len(removed_items)} items from review list.", "removed_items": removed_items},
            status=status.HTTP_200_OK
        )
