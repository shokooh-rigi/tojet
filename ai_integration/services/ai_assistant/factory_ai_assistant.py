from ai_integration.enums import AssistantName
from ai_integration.services.ai_assistant.base_interface import AIAssistant
from ai_integration.services.ai_assistant.cloud_assistant import ClaudeAssistant
from ai_integration.services.ai_assistant.gpt_assistant import GPTAssistant


class AIAssistantFactory:
    """
    Factory class to create AI assistant instances.
    """

    @staticmethod
    def get_assistant(assistant_type: str, **kwargs) -> AIAssistant:
        """
        Create an instance of the desired AI assistant.

        Args:
            assistant_type (str): The type of AI assistant (e.g., 'gpt', 'claude').
            **kwargs: Additional arguments needed for the assistant.

        Returns:
            AIAssistant: An instance of the requested assistant.
        """
        if assistant_type == AssistantName.GPT.value:
            return GPTAssistant(api_key=kwargs.get("api_key"))
        elif assistant_type == AssistantName.CLOUD.value:
            return ClaudeAssistant(api_key=kwargs.get("api_key"))
        else:
            raise ValueError(f"Unknown assistant type: {assistant_type}")
