import anthropic
from ..base import BaseChatbot
from typing import List, Dict
import os
from chatbot.models import Message  # Correct import for the Message model
import logging

class ClaudieChatbot(BaseChatbot):
    def __init__(self, chatbot_data):
        super().__init__(chatbot_data)
        self.client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.character = self.settings.get('character', 'You are a helpful AI assistant.')

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
                temperature=1  # Adding temperature parameter

            )
            assistant_message = response.content[0].text

            return assistant_message
        except Exception as e:
            logging.error(f"Error generating response: {e}")
            return "There was an error processing your request. Please try again."

    def get_settings_schema(self):
        return {
            "character": {
                "type": "string",
                "default": "You are a helpful AI assistant.",
                "description": "The character or system prompt for the chatbot"
            }
        }

    def validate_settings(self, settings):
        if 'character' in settings and not isinstance(settings['character'], str):
            raise ValueError("character must be a string")
        if 'documents' in settings and not isinstance(settings['documents'], list):
            raise ValueError("documents must be a list")
        return settings