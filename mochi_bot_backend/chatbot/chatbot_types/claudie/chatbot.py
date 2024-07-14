import anthropic
from ..base import BaseChatbot
from typing import List, Dict
import os

class ClaudieChatbot(BaseChatbot):
    def __init__(self, chatbot_data):
        super().__init__(chatbot_data)
        self.client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.conversation_history: List[Dict[str, str]] = []
        self.character = self.settings.get('character', 'You are a helpful AI assistant.')
        self.documents = self.settings.get('documents', [])

    def generate_response(self, message_content: str, thread_id: str) -> str:
        self.conversation_history.append({"role": "human", "content": message_content})
        
        context = self._retrieve_relevant_context(message_content)
        
        messages = [
            {"role": "system", "content": self.character},
            *self.conversation_history
        ]
        if context:
            messages.append({"role": "system", "content": f"Relevant context: {context}"})

        response = self.client.messages.create(
            model="claude-3.5-sonnet",
            messages=messages
        )

        assistant_message = response.content[0].text
        self.conversation_history.append({"role": "assistant", "content": assistant_message})
        
        return assistant_message

    def get_settings_schema(self):
        return {
            "character": {
                "type": "string",
                "default": "You are a helpful AI assistant.",
                "description": "The character or system prompt for the chatbot"
            },
            "documents": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "path": {"type": "string"}
                    }
                },
                "description": "Uploaded documents for RAG"
            }
        }

    def validate_settings(self, settings):
        if 'character' in settings and not isinstance(settings['character'], str):
            raise ValueError("character must be a string")
        if 'documents' in settings and not isinstance(settings['documents'], list):
            raise ValueError("documents must be a list")
        return settings

    def _retrieve_relevant_context(self, query: str) -> str:
        # Placeholder implementation
        return "Relevant context from documents would be retrieved here."