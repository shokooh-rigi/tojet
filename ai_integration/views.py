from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from tojet import settings
from .enums import AssistantName
from .services.ai_assistant.factory_ai_assistant import AIAssistantFactory


class AIChatView(APIView):
    """
    API endpoint for AI chat.
    """
    permission_classes = [IsAuthenticated]

    # Define the input and output schema for Swagger documentation
    @swagger_auto_schema(
        operation_summary="Chat with AI Assistant",
        operation_description=(
            "Send a message to the AI assistant and receive a response. "
            "Supports different AI models like GPT and Claude."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "input": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="The user's message or question.",
                    example="What is the Pythagorean theorem?"
                ),
                "assistant_type": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Type of AI assistant to use (e.g., 'gpt', 'claude').",
                    default=AssistantName.GPT.value,
                )
            },
            required=["input"],  # Specify required fields
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "response": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="The AI's response to the user's input."
                    )
                },
            ),
            400: "Bad Request: Invalid input or missing fields.",
        },
    )
    def post(self, request):
        user_input = request.data.get("input")
        assistant_type = request.data.get("assistant_type", AssistantName.GPT.value)
        api_key =settings.GPT_API_KEY

        # Create an AI assistant instance
        try:
            assistant = AIAssistantFactory.get_assistant(assistant_type, api_key=api_key)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)

        # Generate a response
        context = {"system_prompt": "You are a helpful tutor."}
        response = assistant.generate_response(user_input, context)
        return Response({"response": response})
