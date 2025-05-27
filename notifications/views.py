from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from users.models import UserProfile
from .models import Notification, Reminder


class RegisterDeviceTokenView(APIView):
    """
    Registers OneSignal Player ID (device token) for the user.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.data.get("player_id")
        if not token:
            return Response({"error": "Player ID is required."}, status=400)

        user_profile, _ = UserProfile.objects.get_or_create(
            user=request.user
        )
        if token not in user_profile.device_tokens:
            user_profile.device_tokens.append(token)
            user_profile.save()

        return Response({"message": "Player ID registered successfully."}, status=201)

class ReminderView(APIView):
    """
    Lists all reminders for the authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reminders = request.user.reminders.filter(
            is_sent=False
        ).order_by(
            'scheduled_at'
        )
        return Response(
            [{"message": r.message,
              "scheduled_at": r.scheduled_at} for r in reminders],
            status=status.HTTP_200_OK
        )

    def post(self, request):
        message = request.data.get("message")
        scheduled_at = request.data.get("scheduled_at")

        if not message or not scheduled_at:
            return Response(
                {"error": "Message and scheduled_at are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        Reminder.objects.create(
            user=request.user,
            message=message,
            scheduled_at=scheduled_at
        )
        return Response(
            {"message": "Reminder created successfully."},
            status=status.HTTP_201_CREATED
        )

class ListNotificationsView(views.APIView):
    """
    Retrieves all notifications for the authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = request.user.notifications.all().order_by('-scheduled_at')
        return Response(
            [{"title": n.title,
              "message": n.message,
              "is_read": n.is_read} for n in notifications],
            status=status.HTTP_200_OK
        )


class MarkNotificationAsReadView(APIView):
    """
    Mark a specific notification as read.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, notification_id):
        notification = Notification.objects.filter(id=notification_id, user=request.user).first()
        if not notification:
            return Response({"error": "Notification not found."}, status=status.HTTP_404_NOT_FOUND)

        notification.is_read = True
        notification.save()
        return Response({"message": "Notification marked as read."}, status=status.HTTP_200_OK)

class DeleteNotificationView(APIView):
    """
    Delete a specific notification.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, notification_id):
        notification = Notification.objects.filter(id=notification_id, user=request.user).first()
        if not notification:
            return Response({"error": "Notification not found."}, status=status.HTTP_404_NOT_FOUND)

        notification.delete()
        return Response({"message": "Notification deleted successfully."}, status=status.HTTP_200_OK)
