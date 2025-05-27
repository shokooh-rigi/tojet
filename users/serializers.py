from django.contrib.auth import get_user_model
from rest_framework import serializers

from tojet import settings
from .models import Avatar, AvatarBackground, CustomUser
from .validations import validate_iranian_mobile_number, validate_password_strength

User = get_user_model()

class GetOtpSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        max_length=11,
        min_length=11,
        validators=[validate_iranian_mobile_number]
    )


class VerifyOtpSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        max_length=11,
        min_length=11,
        validators=[validate_iranian_mobile_number]
    )
    otp_code = serializers.CharField(max_length=settings.OTP_CODE_DIGITS_COUNT)

    def validate(self, data):
        if not data['otp_code'].isdigit():
            raise serializers.ValidationError({"otp_code": "OTP must be numeric."})
        return data


class CustomUserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(
        max_length=11,
        min_length=11,
        validators=[validate_iranian_mobile_number]
    )
    password = serializers.CharField(
        write_only=True,
        min_length=5,
        validators=[validate_password_strength]
    )
    confirm_password = serializers.CharField(write_only=True)
    referral_code = serializers.CharField(
        required=False,
        allow_blank=True,
        write_only=True,
    )

    class Meta:
        model = CustomUser
        fields = [
            'phone_number',
            'first_name',
            'last_name',
            'password',
            'confirm_password',
            'referral_code',
            'avatar',
            'avatar_background',
        ]

    def validate(self, data):
        # Validate if phone number already exists
        if CustomUser.objects.filter(phone_number=data['phone_number']).exists():
            raise serializers.ValidationError({"phone_number": "A user with this phone number already exists."})

        # Ensure passwords match
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords must match."})

        # Validate referral code
        if data.get('referral_code'):
            referring_user = CustomUser.objects.filter(referral_code=data['referral_code']).first()

            if not referring_user:
                raise serializers.ValidationError({"referral_code": "Invalid referral code."})

            if referring_user.phone_number == data['phone_number']:
                raise serializers.ValidationError({"referral_code": "You cannot refer yourself."})

            # Add referring user to data for further processing
            data['referring_user'] = referring_user

        return data

    def create(self, validated_data):
        # Extract referral code and referring user
        referral_code = validated_data.pop('referral_code', None)
        referring_user = validated_data.pop('referring_user', None)

        # Create user instance
        user = CustomUser.objects.create(
            phone_number=validated_data['phone_number'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            avatar=validated_data.get('avatar'),
            avatar_background=validated_data.get('avatar_background'),
        )

        # Handle referral logic if referring user exists
        if referring_user:
            user.referred_by = referring_user
            user.save()

        return user


class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        max_length=11,
        min_length=11,
        validators=[validate_iranian_mobile_number]
    )
    password = serializers.CharField(
        write_only=True,
        min_length=5,
    )

class UserSetPasswordSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(
        max_length=11,
        min_length=11,
        validators=[validate_iranian_mobile_number]
    )
    password = serializers.CharField(
        write_only=True,
        min_length=5,
        validators=[validate_password_strength],
    )
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['phone_number', 'password', 'confirm_password']

    def validate(self, data):
        # Validate if the phone number exists
        if not CustomUser.objects.filter(phone_number=data['phone_number']).exists():
            raise serializers.ValidationError({"phone_number": "A user with this phone number does not exist."})

        # Validate if passwords match
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords must match."})

        return data

    def update(self, instance, validated_data):
        # Pop the confirm password field for update
        validated_data.pop('confirm_password', None)

        # Set the new password
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ['id','avatar', 'category']


class AvatarBackgroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvatarBackground
        fields = ['id','avatar_background', 'category']
