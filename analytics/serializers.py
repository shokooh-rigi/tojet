from rest_framework import serializers

from .models import Feedback,UserActivityLog


class UserActivityLogSerializer(serializers.ModelSerializer):
    """
    Serializer for user activity logs.
    """
    class Meta:
        model = UserActivityLog
        fields = ['user', 'lesson', 'content', 'activity_type', 'time_spent', 'timestamp']


class FeedbackSerializer(serializers.ModelSerializer):
    """
    Serializer for the Feedback model.
    """
    user = serializers.StringRelatedField()  # Display username instead of ID
    lesson = serializers.StringRelatedField()  # Display lesson title instead of ID

    class Meta:
        model = Feedback
        fields = ['id', 'user', 'lesson', 'rating', 'comments', 'created_at']
        read_only_fields = ['id', 'user', 'lesson', 'created_at']
