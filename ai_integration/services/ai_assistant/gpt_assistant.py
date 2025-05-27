import openai

from ai_integration.services.ai_assistant.base_interface import AIAssistant


class GPTAssistant(AIAssistant):
    """
    Implementation of GPT-based AI Assistant.
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = self.api_key

    def generate_response(self, user_input: str, context: dict = None) -> str:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Specifies the AI model to use. "gpt-3.5-turbo" is optimized for cost-efficiency and high performance.
                messages=[
                    {"role": "system", "content": context.get("system_prompt", "You are a helpful assistant.")},
                    {"role": "user", "content": user_input},
                ],
                temperature=0.7,  # Controls randomness in the response. Higher values (e.g., 1.0) result in more creative and varied responses, while lower values (e.g., 0.2) make the output more focused and deterministic.
                max_tokens=1000,  # The maximum number of tokens (words or word fragments) in the output response. This limits how long the AI's response can be.
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error generating response: {str(e)}"
