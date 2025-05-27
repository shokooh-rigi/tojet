from django.urls import path
from .views import GoalChoicesView, CreateGoalView, ListGoalView, UpdateGoalView
from .views import health_check

urlpatterns = [
    path('goal/choices/', GoalChoicesView.as_view(), name='goal-choices'),
    path('goal/create/', CreateGoalView.as_view(), name='goal-create'),
    path('goal/list/', ListGoalView.as_view(), name='goal-list'),
    path("goal/update/<int:pk>/", UpdateGoalView.as_view(), name="goal-update"),
    path('health/', health_check, name='health_check'),

]
