import anthropic
import os
import logging
from ..base import BaseChatbot
from typing import List, Dict, Any
from chatbot.models import Message  # Correct import for the Message model

class ClaudieChatbot(BaseChatbot):
    def __init__(self, chatbot_data):
        super().__init__(chatbot_data)
        self.client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.character = self.settings.get('character', 'You are a helpful AI assistant.')
        self.temperature = self.settings.get('temperature', 1.0)

    def generate_response(self, message_content: str, thread_id: str) -> str:
        # Fetch all messages related to the thread
        messages = Message.objects.filter(thread_id=thread_id).order_by('created_at')

        # Build the conversation history
        conversation_history = [{"role": msg.role, "content": msg.content} for msg in messages]

        # Debug print the conversation history
        print(f"Debug: Conversation history before sending: {conversation_history}")

        # Send request to the API
        try:
            response = self.client.messages.create(
                system=self.character,
                model="claude-3-5-sonnet-20240620",
                messages=conversation_history,
                max_tokens=1024,
                temperature=self.temperature  # Using temperature setting as a number
            )
            assistant_message = response.content[0].text

            return assistant_message
        except Exception as e:
            logging.error(f"Error generating response: {e}")
            return "There was an error processing your request. Please try again."

    def get_settings_schema(self) -> Dict[str, Any]:
        return {
            "character": {
                "type": "string",
                "default": "You are a helpful AI assistant.",
                "description": "The character or system prompt for the chatbot"
            },
            "temperature": {
                "type": "number",
                "default": 1.0,
                "description": "The temperature setting for the chatbot response, from 0 to 1.",
                "minimum": 0,
                "maximum": 1
            }
        }

    def validate_settings(self, settings: Dict[str, Any]):
        if 'character' in settings and not isinstance(settings['character'], str):
            raise ValueError("character must be a string")
        if 'temperature' in settings:
            if not isinstance(settings['temperature'], (int, float)):
                raise ValueError("temperature must be a number")
            if not (0 <= settings['temperature'] <= 1):
                raise ValueError("temperature must be between 0 and 1")
        return settings

# Example usage
if __name__ == "__main__":
    chatbot_data = {
        "id": "claudie",
        "name": "Claudie",
        "settings": {
            "character": "You are Claudie, a friendly and helpful assistant.",
            "temperature": "0.7"  # Example temperature setting as string
        }
    }

    claudie_chatbot = ClaudieChatbot(chatbot_data)
    response = claudie_chatbot.generate_response("Hello, how can you assist me today?", "thread_123")
    print(response)