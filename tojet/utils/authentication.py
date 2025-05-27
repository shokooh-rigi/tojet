from rest_framework_simplejwt.authentication import JWTAuthentication

def jwt_or_ip_key(request):
    """
    Rate-limit authenticated users by `user_id` (UUID) and fallback to IP address for anonymous users.
    """
    jwt_auth = JWTAuthentication()
    try:
        user, _ = jwt_auth.authenticate(request)
        return str(user.user_id)  # Use user_id (UUID) for authenticated users
    except Exception:
        return request.META.get('REMOTE_ADDR')  # Fallback to IP address for unauthenticated users
