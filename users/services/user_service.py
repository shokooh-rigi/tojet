from django.conf import settings
import logging

from tojet.redis import RedisHandler
from tojet.utils.sms import generate_otp_code
from users.enums import ProviderEnum
from users.models import CustomUser
from users.services.sms_provider.sms_provider_factory import ProviderFactory

logger = logging.getLogger('logger')


class UserService:
    """
    A service class for managing user-related operations, such as sending OTP codes.

    Methods:
        send_otp(phone_number: str) -> dict:
            Generates and sends an OTP to the given phone number using the configured SMS provider.
    """

    def __init__(self):
        pass

    @staticmethod
    def send_otp(phone_number: str) -> dict:
        """
        Generates and sends an OTP code to the specified phone number.

        Steps:
        1. Generate a one-time password (OTP) using the configured digit count.
        2. Store the OTP in Redis with an expiration time.
        3. Use the SMS provider (e.g., Kavenegar) to send the OTP to the user.

        Args:
            phone_number (str): The user's phone number.

        Returns:
            dict: The response from the SMS provider, including status and message.

        Raises:
            Exception: Logs any errors that occur during the process.
        """
        try:
            code = generate_otp_code(digit_count=settings.OTP_CODE_DIGITS_COUNT)

            redis = RedisHandler()
            redis.store(
                key=f'otp:{phone_number}',
                value=code,
                expire_time=settings.OTP_CODE_EXPIRE_TIME,
            )
            logger.info(f"OTP stored in Redis for phone number: {phone_number}")

            # Get the SMS provider instance
            sms_provider = ProviderFactory().create_provider(provider_name=ProviderEnum.KAVENEGAR.value)

            # Send the OTP via the SMS provider
            response = sms_provider.send_sms(phone_number=phone_number, code=code)
            logger.info(f"OTP sent to {phone_number}. Response: {response}")

            return response

        except Exception as e:
            logger.error(f"Failed to send OTP to {phone_number}. Error: {e}")
            raise Exception(f"An error occurred while sending OTP: {e}")

    @staticmethod
    def verify_otp( phone_number: str, otp_code:str) -> bool:
        redis = RedisHandler()
        otp = redis.fetch(key=f'otp:{phone_number}')

        if otp_code != otp:
            return False
        elif otp_code == otp:
            return True
        else:
            return False

