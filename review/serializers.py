from rest_framework import serializers
from review.models import ReviewItem
from lessons.models import Content, Lesson, Syllabus
from exam_tests.models import Question


class ReviewItemSerializer(serializers.ModelSerializer):
    """
    Serializer for ReviewItem model with metadata for user review list items.
    """
    user = serializers.StringRelatedField()  # Display username instead of ID
    metadata = serializers.SerializerMethodField()  # Metadata field for human-readable info

    class Meta:
        model = ReviewItem
        fields = ['id', 'review_type', 'item_id', 'created_at', 'user', 'metadata']

    def get_metadata(self, obj):
        """
        Dynamically fetch human-readable metadata for the item based on review_type.
        """
        if obj.review_type == 'content':
            content = Content.objects.filter(id=obj.item_id).first()
            return {"title": content.name, "description": content.description} if content else None
        elif obj.review_type == 'question':
            question = Question.objects.filter(id=obj.item_id).first()
            return {"text": question.text, "options": question.options} if question else None
        elif obj.review_type == 'lesson':
            lesson = Lesson.objects.filter(id=obj.item_id).first()
            return {"title": lesson.title, "description": lesson.description} if lesson else None
        elif obj.review_type == 'syllabus':
            syllabus = Syllabus.objects.filter(id=obj.item_id).first()
            return {"title": syllabus.title, "lesson": syllabus.lesson.title if syllabus.lesson else None} if syllabus else None
        return None
