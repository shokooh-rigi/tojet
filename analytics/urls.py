from django.urls import path

from .views import (
    AnalyticsView,
    SubmitFeedbackView,
    ListFeedbackView,
    RecommendationView,
    UserAnalyticsView,
    GlobalAnalyticsView,
    UserActivityLogView,
    ReviewAnalyticsView,
)

urlpatterns = [
    path('analytics/', AnalyticsView.as_view(), name='analytics'),
    path('analytics/lessons/<int:lesson_id>/feedback/', SubmitFeedbackView.as_view(), name='submit-feedback'),
    path('analytics/feedback/', ListFeedbackView.as_view(), name='list-feedback'),
    path('analytics/recommendations/', RecommendationView.as_view(), name='recommendations'),
    path('analytics/user/', UserAnalyticsView.as_view(), name='user-analytics'),
    path('analytics/global/', GlobalAnalyticsView.as_view(), name='global-analytics'),
    path('analytics/activities/', UserActivityLogView.as_view(), name='user-activities'),
    path('analytics/review/', ReviewAnalyticsView.as_view(), name='review-analytics'),

]
