from abc import ABC, abstractmethod


class AIAssistant(ABC):
    """
    Abstract base class for AI assistants.
    """

    @abstractmethod
    def generate_response(self, user_input: str, context: dict = None) -> str:
        """
        Generate a response based on user input and optional context.
        """
        pass
