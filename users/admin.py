from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Avatar, AvatarBackground


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        'id',
        'phone_number',
        'first_name',
        'last_name',
        'user_id',
        'avatar',
        'avatar_background',
        'is_active',
        'referral_code',
        'referred_by',
    )
    list_filter = (
        'is_staff',
        'is_active',
        'referred_by',
    )
    search_fields = (
        'phone_number',
        'first_name',
        'last_name',
    )
    ordering = ('date_joined',)
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name',
                       'last_name',
                       'phone_number',
                       'referred_by',
                       'referral_code',
                       ),
        }),
        ('Permissions', {
            'fields': ('is_active',
                       'is_staff',
                       'is_superuser',
                       'groups',
                       'user_permissions'
                       )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined'),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number',
                       'first_name',
                       'last_name',
                       'password1',
                       'password2',
                       'avatar',
                       'avatar_background',
                       'referred_by',
                       ),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)


class AvatarAdmin(admin.ModelAdmin):
    model = Avatar
    list_display = ('avatar', 'category', 'created_at', 'updated_at')
    search_fields = ('category',)
    list_filter = ('category',)
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Avatar, AvatarAdmin)


class AvatarBackgroundAdmin(admin.ModelAdmin):
    model = AvatarBackground
    list_display = ('avatar_background', 'category', 'created_at', 'updated_at')
    search_fields = ('category',)
    list_filter = ('category',)
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(AvatarBackground, AvatarBackgroundAdmin)
