from django.contrib import admin
from .models import Goal, Icon


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'field_of_study',
        'grade',
        'purpose',
        'from_rank_range',
        'to_rank_range',
        'study_hours',
        'created_at',
        'updated_at',
    )

    list_filter = (
        'field_of_study',
        'grade',
        'purpose',
        'study_hours',
        'from_rank_range',
        'to_rank_range',
        'created_at',
    )

    search_fields = (
        'user__username',
        'field_of_study',
        'purpose',
    )

    fields = (
        'user',
        'field_of_study',
        'grade',
        'purpose',
        'from_rank_range',
        'to_rank_range',
        'study_hours',
    )

    # Prepopulate or auto-complete fields if necessary
    autocomplete_fields = ('user',)  # Enables a dropdown/autocomplete for the user field if there are many users
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(Icon)
class IconAdmin(admin.ModelAdmin):
    list_display = (
        'icon_type',
        'choice_value',
        'icon',
        'created_at',
        'updated_at',
    )
    list_filter = ('icon_type',)
    search_fields = ('choice_value',)
