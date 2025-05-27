from django.urls import path
from .views import (
    ListQuestionsView,
    SubmitAnswerView,
    UserStatsView,
    ListExamsView,
)

urlpatterns = [
    path('exams/questions/<int:content_id>/', ListQuestionsView.as_view(), name='list-questions'),
    path('exams/questions/submit/', SubmitAnswerView.as_view(), name='submit-answer'),
    path('exams/user/stats/', UserStatsView.as_view(), name='user-stats'),
    path('exams/', ListExamsView.as_view(), name='list-exams'),
]
