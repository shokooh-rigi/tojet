from django.db import models
from rest_framework import serializers
from .models import Lesson, UserLesson, Grade, Category, SubCategory, Syllabus, Section, Content
from .enums import SectionType, ContentType, UserLessonStatus


# todo : handel it  in related serializer : اگر کاربر کنکور را جزو اهدافش انتخاب کرده باشد، برای هر درس هر سه مقطع(دهم،یازدهم،دوازهم) آن درس به او نمایش داده میشود.


class SyllabusSerializer(serializers.ModelSerializer):
    lesson = serializers.StringRelatedField()

    class Meta:
        model = Syllabus
        fields = [
            'id',
            'title',
            'lesson',
            'order',
            'stars',
            'estimate_study_time',
        ]


class UserLessonSerializer(serializers.ModelSerializer):
    status_label = serializers.CharField(source='get_status_display', read_only=True)
    total_lessons = serializers.SerializerMethodField(read_only=True)  # User's total lessons
    total_estimate_study_time = serializers.SerializerMethodField(read_only=True)  # Total estimate study time
    total_review_lessons = serializers.SerializerMethodField(read_only=True)
    syllabuses = SyllabusSerializer(many=True, source='lesson.syllabus', read_only=True)

    class Meta:
        model = UserLesson
        fields = '__all__'
        read_only_fields = [
            'progress_percentage',
            'last_accessed_at',
            'total_lessons',
            'total_estimate_study_time',
            'total_review_lessons',
            'syllabuses',
        ]

    def get_total_review_lessons(self, obj):
        """
        Calculates the total number of review lessons available for the user
        """
        return UserLesson.objects.filter(
            user=obj.user,
            status__exact=UserLessonStatus.IN_REVIEW.value,
        ).count()

    def get_total_lessons(self, obj):
        """
        Calculates the total number of lessons the user is associated with.
        """
        return UserLesson.objects.filter(user=obj.user).count()

    def get_total_estimate_study_time(self, obj):
        """
        Calculates the total estimated study time for all lessons and their syllabuses associated with the user.
        """
        user_lessons = UserLesson.objects.filter(
            user=obj.user
        ).values_list(
            'lesson',
            flat=True,
        )
        total_time = Syllabus.objects.filter(
            lesson__in=user_lessons
        ).aggregate(
            total_time=models.Sum
                (
                    'estimate_study_time'
                )
        )['total_time'] or 0
        return total_time


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            'id',
            'title',
            'description',
            'grade',
            'category',
            'sub_category'
        ]


class SectionSerializer(serializers.ModelSerializer):
    syllabus = serializers.StringRelatedField()  # Display syllabus title instead of ID
    type_label = serializers.SerializerMethodField()  # Human-readable label for `type`

    class Meta:
        model = Section
        fields = [
            'id',
            'name',
            'syllabus',
            'type',
            'type_label',
            'order'
        ]

    def get_type_label(self, obj):
        return dict(SectionType.choices()).get(obj.type)


class ContentSerializer(serializers.ModelSerializer):
    section = serializers.StringRelatedField()  # Display section name instead of ID
    content_type_label = serializers.SerializerMethodField()  # Human-readable label for `content_type`

    class Meta:
        model = Content
        fields = [
            'id',
            'name',
            'section',
            'content_type',
            'content_type_label',
            'content_url',
            'description',
        ]

    def get_content_type_label(self, obj):
        return dict(ContentType.choices()).get(obj.content_type)

