from django.contrib import admin

from review.models import ReviewItem


@admin.register(ReviewItem)
class ReviewItemAdmin(admin.ModelAdmin):
    """
    Admin configuration for the ReviewItem model.
    """
    list_display = ('id', 'user', 'review_type', 'item_id', 'created_at', 'updated_at')
    list_filter = ('review_type', 'user')
    search_fields = ('user__username', 'review_type', 'item_id')
    ordering = ('user', 'review_type', 'item_id')
