from django.urls import path
from .views import (
    ListSyllabusView,
    ListSectionsView,
    ListContentView,
    TrackProgressView,
    UserDashboardView,
    ListLessonView,
    ListUserReviewLessonsView,
)

urlpatterns = [
    path('lessons/user-reviews/', ListUserReviewLessonsView.as_view(), name='user-review-lessons'),
    path('lessons/', ListLessonView.as_view(), name='list-lessons'),
    path('lessons/syllabus/<int:lesson_id>/', ListSyllabusView.as_view(), name='list-syllabus'),
    path('lessons/sections/<int:syllabus_id>/', ListSectionsView.as_view(), name='list-sections'),
    path('lessons/content/<int:section_id>/', ListContentView.as_view(), name='list-content'),
    path('lessons/progress/track/', TrackProgressView.as_view(), name='track-progress'),
    path('lessons/user-dashboard/', UserDashboardView.as_view(), name='user-dashboard'),
]

