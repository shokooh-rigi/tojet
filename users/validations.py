import os
import re
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
from django.core.files.storage import default_storage

from tojet import settings


def validate_iranian_mobile_number(value):
    """
    Validate Iranian mobile number.
    Must:
    - Start with "09".
    - Be 11 digits long.
    Example: 09121732430.
    """
    mobile_regex = r'^09\d{9}$'  # Starts with '09' and followed by 9 digits (total 11 characters)

    if not re.match(mobile_regex, value):
        raise ValidationError("Phone number must be a valid Iranian mobile number (e.g., 09121732430).")

    return value

def validate_password_strength(password: str):
    """
    Validate the strength of the password.
    Ensures the password is strong and meets defined criteria.
    """
    if len(password) < 8:
        raise ValidationError(_("Password must be at least 8 characters long."))
    if not re.search(r'[a-z]', password):
        raise ValidationError(_("Password must contain at least one lowercase letter."))
    if not re.search(r'[A-Z]', password):
        raise ValidationError(_("Password must contain at least one uppercase letter."))
    if not re.search(r'\d', password):
        raise ValidationError(_("Password must contain at least one number."))
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError(_("Password must contain at least one special character."))


def validate_file_extension(value):
    """
     Validator for file extensions (using settings from settings.py)
    """
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in settings.IMAGE_ALLOWED_EXTENSIONS:
        raise ValidationError(f"File extension not allowed. Allowed extensions: {', '.join(settings.ALLOWED_IMAGE_EXTENSIONS)}")


def validate_file_size(value):
    """
    Validator for file size (using settings from settings.py)
    """
    if value.size > settings.IMAGE_MAX_UPLOAD_SIZE:
        raise ValidationError(f"File size exceeds {settings.IMAGE_MAX_UPLOAD_SIZE // (1024 * 1024)}MB.")


def validate_unique_file(value):
    """
    Validator for unique file based on filename
    """
    if default_storage.exists(value.name):
        raise ValidationError("A file with this name already exists.")
