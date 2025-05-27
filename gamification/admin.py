from django.contrib import admin
from .models import Leaderboard


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    """
    Admin interface for Leaderboard model.
    """
    list_display = ('user', 'points', 'rank', 'last_updated')
    list_filter = ('rank', 'last_updated')
    search_fields = ('user__username',)
    ordering = ('rank',)
    readonly_fields = ('last_updated',)
    fieldsets = (
        (None, {
            'fields': ('user', 'points', 'rank')
        }),
        ('Timestamps', {
            'fields': ('last_updated',),
        }),
    )
