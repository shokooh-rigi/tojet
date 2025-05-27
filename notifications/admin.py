from django.contrib import admin
from .models import Notification, Reminder


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Admin interface for Notification model.
    """
    list_display = ('user', 'title', 'notification_type', 'is_read', 'scheduled_at', 'created_at')
    list_filter = ('is_read', 'notification_type', 'scheduled_at', 'created_at')
    search_fields = ('user__username', 'title', 'message')
    ordering = ('-scheduled_at',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('user', 'title', 'message', 'notification_type')
        }),
        ('Status', {
            'fields': ('is_read', 'scheduled_at', 'created_at', 'updated_at'),
        }),
    )


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    """
    Admin interface for Reminder model.
    """
    list_display = ('user', 'message', 'scheduled_at', 'is_sent', 'created_at')
    list_filter = ('is_sent', 'scheduled_at', 'created_at')
    search_fields = ('user__username', 'message')
    ordering = ('-scheduled_at',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('user', 'message', 'scheduled_at')
        }),
        ('Status', {
            'fields': ('is_sent', 'created_at', 'updated_at'),
        }),
    )
