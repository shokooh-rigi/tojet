from celery.bin.upgrade import settings
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer


class PostView(APIView):
    """
    Handles creating, listing, updating, and deleting posts.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List all posts",
        operation_description="Retrieve a paginated list of posts, ordered by creation date.",
        responses={200: PostSerializer(many=True)},
    )
    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 10
        posts = Post.objects.all().order_by('-created_at')
        result_page = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create a post",
        operation_description="Create a new post with content and an optional image.",
        request_body=PostSerializer,
        responses={201: PostSerializer, 400: "Validation Error"},
    )
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Update a post",
        operation_description="Update the content or image of a specific post created by the authenticated user.",
        request_body=PostSerializer,
        manual_parameters=[
            openapi.Parameter(
                'post_id', openapi.IN_PATH, description="ID of the post to update", type=openapi.TYPE_INTEGER
            ),
        ],
        responses={200: PostSerializer, 404: "Post not found", 400: "Validation Error"},
    )
    def put(self, request, post_id):
        post = Post.objects.filter(id=post_id, user=request.user).first()
        if not post:
            return Response({"error": "Post not found or unauthorized"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete a post",
        operation_description="Delete a specific post created by the authenticated user.",
        manual_parameters=[
            openapi.Parameter(
                'post_id', openapi.IN_PATH, description="ID of the post to delete", type=openapi.TYPE_INTEGER
            ),
        ],
        responses={200: "Post deleted successfully", 404: "Post not found"},
    )
    def delete(self, request, post_id):
        post = Post.objects.filter(id=post_id, user=request.user).first()
        if not post:
            return Response({"error": "Post not found or unauthorized"}, status=status.HTTP_404_NOT_FOUND)

        post.delete()
        return Response({"message": "Post deleted successfully"}, status=status.HTTP_200_OK)


class CommentView(APIView):
    """
    Handles creating, listing, updating, and deleting comments for a specific post.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List comments for a post",
        operation_description="Retrieve a paginated list of comments for a specific post.",
        manual_parameters=[
            openapi.Parameter(
                'post_id', openapi.IN_PATH, description="ID of the post", type=openapi.TYPE_INTEGER
            ),
        ],
        responses={200: CommentSerializer(many=True)},
    )
    def get(self, request, post_id):
        paginator = PageNumberPagination()
        paginator.page_size = 10
        comments = Comment.objects.filter(post_id=post_id).order_by('created_at')
        result_page = paginator.paginate_queryset(comments, request)
        serializer = CommentSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create a comment",
        operation_description="Create a new comment for a specific post.",
        request_body=CommentSerializer,
        manual_parameters=[
            openapi.Parameter(
                'post_id', openapi.IN_PATH, description="ID of the post", type=openapi.TYPE_INTEGER
            ),
        ],
        responses={201: CommentSerializer, 400: "Validation Error"},
    )
    def post(self, request, post_id):
        data = request.data
        data['post'] = post_id
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Update a comment",
        operation_description="Update the content of a specific comment created by the authenticated user.",
        request_body=CommentSerializer,
        manual_parameters=[
            openapi.Parameter(
                'post_id', openapi.IN_PATH, description="ID of the post", type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'comment_id', openapi.IN_PATH, description="ID of the comment to update", type=openapi.TYPE_INTEGER
            ),
        ],
        responses={200: CommentSerializer, 404: "Comment not found", 400: "Validation Error"},
    )
    def put(self, request, post_id, comment_id):
        comment = Comment.objects.filter(id=comment_id, post_id=post_id, user=request.user).first()
        if not comment:
            return Response({"error": "Comment not found or unauthorized"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete a comment",
        operation_description="Delete a specific comment created by the authenticated user.",
        manual_parameters=[
            openapi.Parameter(
                'post_id', openapi.IN_PATH, description="ID of the post", type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'comment_id', openapi.IN_PATH, description="ID of the comment to delete", type=openapi.TYPE_INTEGER
            ),
        ],
        responses={200: "Comment deleted successfully", 404: "Comment not found"},
    )
    def delete(self, request, post_id, comment_id):
        comment = Comment.objects.filter(id=comment_id, post_id=post_id, user=request.user).first()
        if not comment:
            return Response({"error": "Comment not found or unauthorized"}, status=status.HTTP_404_NOT_FOUND)

        comment.delete()
        return Response({"message": "Comment deleted successfully"}, status=status.HTTP_200_OK)



class LikeView(APIView):
    """
    Toggles likes on posts and comments.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Toggle like",
        operation_description="Like or unlike a post or comment.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'type': openapi.Schema(type=openapi.TYPE_STRING, description="'post' or 'comment'"),
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the post or comment"),
            },
        ),
        responses={
            201: openapi.Response("Liked"),
            200: openapi.Response("Unliked"),
            400: "Invalid type",
            404: "Item not found",
        },
    )
    def post(self, request):
        like_type = request.data.get('type')  # "post" or "comment"
        item_id = request.data.get('id')

        if like_type == "post":
            obj = Post.objects.filter(id=item_id).first()
        elif like_type == "comment":
            obj = Comment.objects.filter(id=item_id).first()
        else:
            return Response({"error": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)

        if not obj:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        # Toggle like
        like, created = Like.objects.get_or_create(user=request.user, **{f"{like_type}": obj})
        if not created:
            like.delete()
            return Response({"message": f"Unliked {like_type}"}, status=status.HTTP_200_OK)

        return Response({"message": f"Liked {like_type}"}, status=status.HTTP_201_CREATED)