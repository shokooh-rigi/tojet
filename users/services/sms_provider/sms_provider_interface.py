from abc import ABC, abstractmethod


class IProvider(ABC):
    """
    Abstract base class representing an SMS provider interface for OTP management.

    Subclasses should implement methods to handle sending SMS and other provider-specific actions.
    """

    @abstractmethod
    def send_sms(self, phone_number: str, code: str) -> dict:
        """
        Abstract method to send an SMS to a given phone number.

        Args:
            phone_number (str): The recipient's phone number (must be valid).
            code (str): The activation code or message to send.

        Returns:
            dict: The response from the SMS provider (e.g., a JSON object or status).
        """
        pass
