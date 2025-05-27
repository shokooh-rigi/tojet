from rest_framework import serializers
from exam_tests.models import Question, UserAnswer, Exam


class QuestionSerializer(serializers.ModelSerializer):
    content = serializers.StringRelatedField()  # Display content name instead of ID

    class Meta:
        model = Question
        fields = [
            'id',
            'text',
            'options',
            'correct_answer',
            'explanation',
            'difficulty',
            'tags',
            'score',
            'content',
        ]


class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = [
            'id',
            'user',
            'question',
            'selected_option',
            'is_correct',
            'answered_at',
            'time_taken',
            'attempt_number',
        ]


class ExamSerializer(serializers.ModelSerializer):
    total_questions = serializers.IntegerField(read_only=True)

    class Meta:
        model = Exam
        fields = [
            'id',
            'title',
            'created_by',
            'questions',
            'duration',
            'total_questions',
        ]
