from celery import shared_task
import logging

from users.services.user_service import UserService

logger = logging.getLogger(__name__)


@shared_task
def send_otp_task(phone_number: str):
    """
    Celery task for sending OTP to the provided phone number.

    This task is called asynchronously and uses the UserService to generate
    the OTP, store it in Redis, and send it via SMS.

    :param phone_number: The phone number to which the OTP will be sent.
    :raises Exception: If any error occurs during the OTP sending process.
    """
    try:
        logger.info(f"Starting OTP sending task for phone number: {phone_number}")

        service = UserService()
        service.send_otp(phone_number)

        logger.info(f"OTP sent successfully to {phone_number}")

    except Exception as e:
        logger.error(f"Failed to send OTP for phone number {phone_number}. Error: {e}")
        raise e
