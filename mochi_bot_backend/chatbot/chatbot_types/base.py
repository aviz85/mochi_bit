from abc import ABC, abstractmethod
import anthropic
import os
import logging
from typing import List, Dict, Any

class BaseChatbot(ABC):
    def __init__(self, chatbot_data):
        self.id = chatbot_data['id']
        self.name = chatbot_data['name']
        self.settings = self.convert_settings(chatbot_data['settings'], self.get_settings_schema())

    @abstractmethod
    def generate_response(self, message_content: str, thread_id: str) -> str:
        pass

    @abstractmethod
    def get_settings_schema(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def validate_settings(self, settings: Dict[str, Any]):
        pass

    def convert_settings(self, settings: Dict[str, Any], schema: Dict[str, Any]) -> Dict[str, Any]:
        converted_settings = {}
        for key, value in settings.items():
            if key in schema:
                expected_type = schema[key].get('type')
                if expected_type == 'number':
                    converted_settings[key] = float(value)
                elif expected_type == 'integer':
                    converted_settings[key] = int(value)
                elif expected_type == 'boolean':
                    converted_settings[key] = bool(value)
                else:
                    converted_settings[key] = value  # Default to original value for unknown types
            else:
                converted_settings[key] = value  # If not in schema, keep as is
        return converted_settings