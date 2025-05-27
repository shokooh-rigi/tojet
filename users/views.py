from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django_ratelimit.decorators import ratelimit
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.exceptions import ValidationError
from tojet.utils.authentication import jwt_or_ip_key

from .models import Avatar, AvatarBackground, CustomUser
from .services.avatar_service import AvatarService
from .tasks import send_otp_task
from .services.user_service import UserService
from .serializers import GetOtpSerializer, VerifyOtpSerializer, UserLoginSerializer, \
    UserSetPasswordSerializer, AvatarSerializer, AvatarBackgroundSerializer, CustomUserSerializer


class UserGetOtpView(APIView):
    """
    View for handling OTP generation and sending.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Request OTP",
        operation_description="Generates and sends an OTP to the provided phone number.",
        request_body=GetOtpSerializer,  # Use the serializer directly
        responses={
            202: openapi.Response(
                description="OTP generation in progress.",
                examples={"application/json": {"message": "OTP generation in progress"}},
            ),
            400: openapi.Response(
                description="Validation error.",
                examples={"application/json": {"phone_number": ["This field is required."]}},
            ),
        }
    )
    def post(self, request):
        serializer = GetOtpSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']

            service = UserService()
            service.send_otp(phone_number)
            # send_otp_task.delay(phone_number)
            return Response(
                data={"message": "OTP generation in progress"},
                status=status.HTTP_202_ACCEPTED
            )
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class UserVerifyOtpView(APIView):
    """
    View for handling OTP verification.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Verify OTP",
        operation_description="Verifies the provided OTP for the given phone number.",
        request_body=VerifyOtpSerializer,  # Use the serializer directly
        responses={
            200: openapi.Response(
                description="OTP verified successfully.",
                examples={"application/json": {"message": "OTP verified successfully"}},
            ),
            400: openapi.Response(
                description="Invalid OTP or validation error.",
                examples={"application/json": {"message": "Invalid OTP"}},
            ),
        }
    )
    def post(self, request):
        serializer = VerifyOtpSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            otp_code = serializer.validated_data['otp_code']

            user_service = UserService()
            result = user_service.verify_otp(
                phone_number=phone_number,
                otp_code=otp_code,
            )
            if result:
                return Response(
                    data={"message": "OTP verified successfully"},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    data={"message": "Invalid OTP"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class UserSignUpView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="User Registration",
        operation_description=(
            "Allows users to register by providing their details (e.g., phone number, password). "
            "The data is validated using the `UserSignUpSerializer`. If the data is valid, "
            "the user is registered, and a success message is returned."
        ),
        request_body=CustomUserSerializer,
        responses={
            201: openapi.Response(
                description="User registered successfully.",
                examples={"application/json": {"message": "User registered successfully"}},
            ),
            400: openapi.Response(
                description="Validation error.",
                examples={"application/json": {"phone_number": ["This field is required."]}},
            ),
        }
    )
    def post(self, request):
        """
        Handles user registration.
        """
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={"message": "User registered successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UserLoginView(APIView):
    permission_classes = []

    @swagger_auto_schema(
        operation_summary="User Login",
        operation_description=(
            "Allows users to log in by providing their phone number and password. "
        ),
        request_body=UserLoginSerializer,
        responses={
            200: openapi.Response(
                description="User login successful.",
                examples={"application/json": {"message": "User login successful"}},
            ),
            401: openapi.Response(
                description="Invalid credentials.",
                examples={"application/json": {"error": "Invalid phone number or password"}},
            ),
            400: openapi.Response(
                description="Validation error.",
                examples={"application/json": {"phone_number": ["This field is required."]}},
            ),
        }
    )
    #todo: correct method issue: @ratelimit(key=jwt_or_ip_key, rate='8/m', method='POST', block=True)
    def post(self, request):
        """
        Handles user login.
        """
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            password = serializer.validated_data['password']

            user = authenticate(username=phone_number, password=password)
            if user is not None:
                return Response(
                    data={"message": "User login successful"},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    data={"error": "Invalid phone number or password"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class UserSetPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Set Password",
        operation_description=(
            "Allows authenticated users to set their password if they forget it. "
            "Users must provide their phone number, new password, and confirm password."
        ),
        request_body=UserSetPasswordSerializer,
        responses={
            200: openapi.Response(
                description="Password set successfully.",
                examples={"application/json": {"message": "User set password successfully"}},
            ),
            400: openapi.Response(
                description="Validation error.",
                examples={"application/json": {"password": ["This field is required."]}},
            ),
        }
    )
    def post(self, request):
        """
        Allows authenticated users to change their password.
        """
        serializer = UserSetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = CustomUser.objects.get(phone_number=request.data['phone_number'])
            serializer.update(user, serializer.validated_data)  # Update the password for the user
            return Response(
                data={"message": "Password set successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="User Logout",
        operation_description="Logs the user out by removing their refresh token on the client-side.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh_token': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="The refresh token (not used in this example, only to represent the user's session)."
                ),
            },
            required=['refresh_token'],
        ),
        responses={
            200: openapi.Response(
                description="User logged out successfully.",
                examples={"application/json": {"message": "User logged out successfully"}},
            ),
            400: openapi.Response(
                description="Invalid or missing refresh token.",
                examples={
                    "application/json": {
                        "message": "Refresh token is required."
                    }
                },
            ),
        }
    )
    def post(self, request):
        """
        Simple logout endpoint that does not invalidate tokens but removes the session from the client.
        """
        try:
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response(
                    data={"message": "Refresh token is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Here you just acknowledge the logout process without blacklisting or rotating the token.
            # You can clear the session on the client side (e.g., in the frontend).

            return Response(
                data={"message": "User logged out successfully"},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                data={"message": "Something went wrong.", "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserAvatarsView(APIView):
    # permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Fetch all avatars with pagination and optional category filtering",
        manual_parameters=[
            openapi.Parameter(
                'page_size', openapi.IN_QUERY, description="Number of avatars per page", type=openapi.TYPE_INTEGER, default=10
            ),
            openapi.Parameter(
                'page_number', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER, default=1
            ),
            openapi.Parameter(
                'category', openapi.IN_QUERY, description="Filter avatars by category", type=openapi.TYPE_STRING, required=False
            ),
        ],
        responses={
            200: openapi.Response(
                description="Paginated list of avatars",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'total_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'total_pages': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'current_page': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'page_size': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'avatars': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=AvatarSerializer().to_representation(Avatar()),
                        ),
                    }
                )
            ),
            400: openapi.Response(description="Invalid parameters")
        }
    )
    def get(self, request):
        # Get query parameters for pagination and filtering
        page_size = int(request.query_params.get('page_size', 10))  # Default to 10 items per page
        page_number = int(request.query_params.get('page_number', 1))  # Default to the first page
        category = request.query_params.get('category', None)  # Optional filter by category

        # Validate page_size and page_number
        if page_size <= 0 or page_number <= 0:
            raise ValidationError("Page size and page number must be positive integers")

        # Fetch avatars using the service layer
        result = AvatarService.get_avatars(
            page_number=page_number,
            page_size=page_size,
            category=category,
        )

        # Return paginated response
        return Response({
            'total_count': result['total_count'],
            'total_pages': result['total_pages'],
            'current_page': result['current_page'],
            'page_size': result['page_size'],
            'avatars': result['avatars']
        }, status=status.HTTP_200_OK)


class UserBackgroundAvatarsView(APIView):
    # permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Fetch background avatars with pagination and optional category filtering",
        manual_parameters=[
            openapi.Parameter(
                'page_size', openapi.IN_QUERY, description="Number of background avatars per page", type=openapi.TYPE_INTEGER, default=10
            ),
            openapi.Parameter(
                'page_number', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER, default=1
            ),
            openapi.Parameter(
                'category', openapi.IN_QUERY, description="Filter background avatars by category", type=openapi.TYPE_STRING, required=False
            ),
        ],
        responses={
            200: openapi.Response(
                description="Paginated list of background avatars",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'total_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'total_pages': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'current_page': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'page_size': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'background_avatars': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=AvatarBackgroundSerializer().to_representation(AvatarBackground()),
                        ),
                    }
                )
            ),
            400: openapi.Response(description="Invalid parameters")
        }
    )
    def get(self, request):
        # Get query parameters for pagination and filtering
        page_size = int(request.query_params.get('page_size', settings.PAGE_SIZE))
        page_number = int(request.query_params.get('page_number', 1))  # Default to the first page
        category = request.query_params.get('category', None)

        # Validate page_size and page_number
        if page_size <= 0 or page_number <= 0:
            raise ValidationError("Page size and page number must be positive integers")

        result = AvatarService.get_avatar_backgrounds(
            page_number=page_number,
            page_size=page_size,
            category=category
        )

        # Return paginated response
        return Response({
            'total_count': result['total_count'],
            'total_pages': result['total_pages'],
            'current_page': result['current_page'],
            'page_size': result['page_size'],
            'background_avatars': result['background_avatars']
        }, status=status.HTTP_200_OK)

