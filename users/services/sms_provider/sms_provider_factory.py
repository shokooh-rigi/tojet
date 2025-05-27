import logging

from users.enums import ProviderEnum
from users.services.sms_provider.kavenegar_provider import KavenegarProvider
from users.services.sms_provider.sms_provider_interface import IProvider

logger = logging.getLogger(__name__)


class ProviderFactory:
    """
    Factory class responsible for creating provider instances based on the provider name.
    """

    @staticmethod
    def create_provider(provider_name: str) -> IProvider:
        """
        Create and return an instance of a provider based on the provider name.

        Args:
            provider_name (str): The name of the provider.

        Returns:
            IProvider: An instance of a provider that implements IProvider.

        Raises:
            ValueError: If the provider name is not recognized.
        """
        if provider_name == ProviderEnum.KAVENEGAR.value:
            return KavenegarProvider()

        logger.error(f"Unknown provider: {provider_name}")
        raise ValueError(f"Unknown provider: {provider_name}")
