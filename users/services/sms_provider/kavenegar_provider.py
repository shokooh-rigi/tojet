import requests
import logging
from tojet import settings
from users.services.sms_provider.sms_provider_interface import IProvider

logger = logging.getLogger(__name__)


class KavenegarProvider(IProvider):
    """
    Provider implementation for the Kavenegar SMS service. This class handles sending SMS
    using the Kavenegar API.
    """

    def __init__(self):
        """
        Initialize the KavenegarProvider with the base URL from settings.
        """
        self.BASE_URL = settings.KAVENEGAR_BASE_URL

    def send_sms(self, phone_number: str, code: str) -> dict:
        """
        Send an SMS to the given phone number using the Kavenegar API.

        Args:
            phone_number (str): The recipient's phone number (must be valid).
            code (str): The activation code to send.

        Returns:
            dict: A JSON response from the Kavenegar API if successful, or an empty dictionary on failure.

        Raises:
            requests.RequestException: If an error occurs during the API call.
        """
        try:
            url = f'{self.BASE_URL}{settings.KAVENEGAR_API_KEY}{settings.KAVENEGAR_SEND_SMS_PATH}'
            message = f'کد فعالسازی توجت: {code}'
            data = {
                'sender': settings.KAVENEGAR_SENDING_NUMBER,
                'receptor': phone_number,
                'message': message,
            }
            response = requests.post(
                url=url,
                data=data,
            )
            response.raise_for_status()
            logger.info(f"SMS sent successfully to {phone_number}")
            return response.json()

        except requests.RequestException as e:
            logger.error(f"Error in sending Kavenegar SMS to {phone_number}: {e}")
            return {}
