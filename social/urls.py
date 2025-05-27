from django.urls import path
from .views import PostView, CommentView, LikeView

urlpatterns = [
    path('social/posts/', PostView.as_view(), name='posts'),
    path('social/posts/<int:post_id>/comments/', CommentView.as_view(), name='post-comments'),
    path('social/likes/', LikeView.as_view(), name='likes'),
]
