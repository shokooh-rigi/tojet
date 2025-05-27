from django.contrib import admin
from analytics.models import UserActivityLog, Feedback, Recommendation


@admin.register(UserActivityLog)
class UserActivityLogAdmin(admin.ModelAdmin):
    """
    Admin configuration for the UserActivityLog model.
    """
    list_display = (
        'id',
        'user',
        'activity_type',
        'lesson',
        'content',
        'time_spent',
        'timestamp',
    )
    search_fields = ('user__username', 'lesson__title', 'content__name')
    list_filter = ('activity_type', 'timestamp')
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)
    fieldsets = (
        (None, {
            'fields': ('user', 'activity_type', 'lesson', 'content', 'time_spent')
        }),
        ('Timestamps', {
            'fields': ('timestamp',)
        }),
    )


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Feedback model.
    """
    list_display = (
        'id',
        'user',
        'lesson',
        'rating',
        'comments',
        'created_at',
        'updated_at',
    )
    search_fields = ('user__username', 'lesson__title', 'comments')
    list_filter = ('rating', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('user', 'lesson', 'rating', 'comments')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Recommendation model.
    """
    list_display = (
        'id',
        'user',
        'lesson',
        'reason',
        'created_at',
        'updated_at',
    )
    search_fields = ('user__username', 'lesson__title', 'reason')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('user', 'lesson', 'reason')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
