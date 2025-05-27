from django.contrib import admin
from .models import (
    Grade,
    Category,
    SubCategory,
    Lesson,
    Syllabus,
    Section,
    Content,
    UserLesson
)


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Grade model.
    """
    list_display = ('id', 'name', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Category model.
    """
    list_display = ('id', 'name', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the SubCategory model.
    """
    list_display = ('id', 'name', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Lesson model.
    """
    list_display = ('id', 'title', 'grade', 'category', 'sub_category', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('grade', 'category', 'sub_category')
    ordering = ('title',)


@admin.register(Syllabus)
class SyllabusAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Syllabus model.
    """
    list_display = ('id', 'title', 'lesson', 'order', 'created_at', 'updated_at')
    search_fields = ('title',)
    list_filter = ('lesson',)
    ordering = ('lesson', 'order')


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Section model.
    """
    list_display = ('id', 'name', 'syllabus', 'type', 'order', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('syllabus', 'type')
    ordering = ('syllabus', 'order')


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Content model.
    """
    list_display = ('id', 'name', 'section', 'content_type', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('section', 'content_type')
    ordering = ('section', 'name')


@admin.register(UserLesson)
class UserLessonAdmin(admin.ModelAdmin):
    """
    Admin configuration for the UserLesson model.
    """
    list_display = (
        'id',
        'user',
        'lesson',
        'status',
        'progress_percentage',
        'last_accessed_at',
        'created_at',
        'updated_at',
        'points_earned',
    )
    list_filter = ('status', 'lesson', 'user')
    search_fields = ('user__username', 'lesson__title')
    ordering = ('user', 'lesson', 'status')
