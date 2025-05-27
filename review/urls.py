from django.urls import path
from .views import (
    AddReviewItemView,
    ListReviewItemsView,
    RemoveReviewItemView,
)

urlpatterns = [
    path('reviews/add/', AddReviewItemView.as_view(), name='add-review-item'),
    path('reviews/list/', ListReviewItemsView.as_view(), name='list-review-items'),
    path('reviews/remove/', RemoveReviewItemView.as_view(), name='remove-review-item'),
]

