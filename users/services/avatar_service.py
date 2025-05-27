from django.core.paginator import Paginator
from django.db.models import Q

from tojet import settings
from users.models import Avatar, AvatarBackground
from users.serializers import AvatarSerializer, AvatarBackgroundSerializer


class AvatarService:
    @staticmethod
    def get_avatars(
            page_number=1,
            page_size=settings.PAGE_SIZE,
            category=None
    ):
        # Start with all avatars
        avatars = Avatar.objects.all()

        # Apply category filter if provided
        if category:
            avatars = avatars.filter(category=category)

        # Paginate the results
        paginator = Paginator(avatars, page_size)
        page = paginator.get_page(page_number)
        serialized_data = AvatarSerializer(page.object_list, many=True).data
        # Return paginated data
        return {
            'total_count': paginator.count,
            'total_pages': paginator.num_pages,
            'current_page': page.number,
            'page_size': page_size,
            'avatars': serialized_data,
        }

    @staticmethod
    def get_avatar_backgrounds(
            page_number=1,
            page_size=settings.PAGE_SIZE,
            category=None
    ):
        # Start with all  avatar backgrounds
        avatar_backgrounds = AvatarBackground.objects.all()

        # Apply category filter if provided
        if category:
            avatar_backgrounds = avatar_backgrounds.filter(category=category)

        # Paginate the results
        paginator = Paginator(avatar_backgrounds, page_size)
        page = paginator.get_page(page_number)
        serialized_data = AvatarBackgroundSerializer(page.object_list, many=True).data

        # Return paginated data
        return {
            'total_count': paginator.count,
            'total_pages': paginator.num_pages,
            'current_page': page.number,
            'page_size': page_size,
            'background_avatars': serialized_data
        }