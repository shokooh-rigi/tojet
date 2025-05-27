import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.db.models import SET_NULL

from tojet.base_model import BaseModel
from users.validations import validate_iranian_mobile_number, validate_file_extension, validate_file_size, \
    validate_unique_file


class CustomUser(AbstractUser, BaseModel):
    phone_number = models.CharField(
        max_length=11,
        unique=True,
        validators=[validate_iranian_mobile_number],
        help_text=' User mobile : Example:=09905432234',
    )
    avatar = models.ForeignKey(
        to='Avatar',
        on_delete=SET_NULL,
        blank=True,
        null=True,
    )
    avatar_background = models.ForeignKey(
        to='AvatarBackground',
        on_delete=SET_NULL,
        null=True,
        blank=True,
    )
    user_id = models.UUIDField(
        editable=False,
        max_length=36,
        default=uuid.uuid4,
        help_text="A unique identifier for the user, automatically generated.",
    )
    referral_code = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True,
    )
    referred_by = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='referrals',
    )

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = str(uuid.uuid4())
        if not self.referral_code:
            self.referral_code = self._generate_referral_code()
        super().save(*args, **kwargs)

    def _generate_referral_code(self):
        import random
        import string
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


class Avatar(BaseModel):
    avatar = models.ImageField(
        upload_to=settings.AVATAR_PATH,
        validators=[
            validate_file_extension,
            validate_file_size,
            validate_unique_file,
        ]
    )
    category = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.avatar)


class AvatarBackground(BaseModel):
    avatar_background = models.ImageField(
        upload_to=settings.AVATAR_BACKGROUND_PATH,
        validators=[
            validate_file_extension,
            validate_file_size,
            validate_unique_file,
        ]
    )
    category = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.avatar_background)


class UserProfile(BaseModel):
    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
