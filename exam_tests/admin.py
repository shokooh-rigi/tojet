from django.contrib import admin
from exam_tests.models import Question, UserAnswer, Exam


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'text',
        'content',
        'is_ai_generated',
        'difficulty',
        'created_at',
    )
    search_fields = ('text',)
    list_filter = (
        'content',
        'is_ai_generated',
        'difficulty',
        'created_at'
    )
    ordering = ('-created_at',)


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'question',
        'is_correct',
        'answered_at',
        'time_taken',
    )
    search_fields = ('user__username', 'question__text')
    list_filter = ('is_correct', 'answered_at')
    ordering = ('-answered_at',)


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'created_by',
        'duration',
        'total_questions',
    )
    search_fields = ('title',)
    list_filter = ('created_by',)
