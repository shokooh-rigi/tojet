from onesignal_sdk.client import Client

from tojet import settings


class OneSignalClient:
    """
    Helper class to send push notifications via OneSignal.
    """
    def __init__(self):
        self.client = Client(
            app_id=settings.ONESIGNAL_APP_ID,
            rest_api_key=settings.ONESIGNAL_API_KEY,
        )

    def send_notification(
            self,
            title,
            message,
            user_ids=None,
            data=None
    ):
        """
        Send a push notification to specified users or segments.

        Args:
            title (str): Notification title.
            message (str): Notification body.
            user_ids (list): List of OneSignal player IDs (device tokens).
            data (dict): Additional data to include in the notification.
        """
        try:
            notification = {
                "headings": {"en": title},
                "contents": {"en": message},
                "include_player_ids": user_ids,  # Send to specific users
                "data": data or {}
            }
            response = self.client.send_notification(notification)
            return response
        except Exception as e:
            return {"error": str(e)}
