from django.urls import path

from users.views import (
    UserSignUpView,
    UserGetOtpView,
    UserVerifyOtpView,
    UserLoginView,
    UserSetPasswordView,
    UserAvatarsView,
    UserBackgroundAvatarsView,
    UserLogoutView,

)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('get-otp/', UserGetOtpView.as_view(), name='user-get-otp'),
    path('verify-otp/', UserVerifyOtpView.as_view(), name='user-verify-otp'),
    path('signup/', UserSignUpView.as_view(), name='user-signup'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('set-password/', UserSetPasswordView.as_view(), name='user-set-password'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('avatars/', UserAvatarsView.as_view(), name='user-avatars'),
    path('background-avatars/', UserBackgroundAvatarsView.as_view(), name='user-background-avatars'),

]