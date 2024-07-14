import os
import json
from importlib import import_module
from typing import Dict, Any, List

class ChatbotFactory:
    _chatbot_types: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def register_chatbot_types(cls) -> None:
        chatbot_types_dir = os.path.join(os.path.dirname(__file__), 'chatbot_types')
        for type_folder in os.listdir(chatbot_types_dir):
            type_path = os.path.join(chatbot_types_dir, type_folder)
            if os.path.isdir(type_path):
                metadata_path = os.path.join(type_path, 'metadata.json')
                if os.path.exists(metadata_path):
                    try:
                        with open(metadata_path, 'r') as f:
                            metadata = json.load(f)
                        chatbot_module = import_module(f'.chatbot_types.{type_folder}.chatbot', package='chatbot')
                        chatbot_class = getattr(chatbot_module, f"{metadata['name']}Chatbot")
                        cls._chatbot_types[metadata['type']] = {
                            'class': chatbot_class,
                            'metadata': metadata
                        }
                    except (json.JSONDecodeError, ImportError, AttributeError) as e:
                        print(f"Error loading chatbot type {type_folder}: {str(e)}")

    @classmethod
    def create_chatbot(cls, chatbot_data: Dict[str, Any]) -> Any:
        if not cls._chatbot_types:
            cls.register_chatbot_types()
        
        chatbot_type = chatbot_data.get('chatbot_type')
        if not chatbot_type:
            raise ValueError("chatbot_type is required in chatbot_data")
        
        if chatbot_type not in cls._chatbot_types:
            raise ValueError(f"Unknown chatbot type: {chatbot_type}")
        
        return cls._chatbot_types[chatbot_type]['class'](chatbot_data)

    @classmethod
    def get_chatbot_metadata(cls, chatbot_type: str) -> Dict[str, Any]:
        if not cls._chatbot_types:
            cls.register_chatbot_types()
        
        if chatbot_type not in cls._chatbot_types:
            raise ValueError(f"Unknown chatbot type: {chatbot_type}")
        
        return cls._chatbot_types[chatbot_type]['metadata']

    @classmethod
    def get_all_chatbot_types(cls) -> List[Dict[str, str]]:
        if not cls._chatbot_types:
            cls.register_chatbot_types()
        
        return [
            {'type': chatbot_type, 'name': info['metadata']['name'], 'description': info['metadata']['description']}
            for chatbot_type, info in cls._chatbot_types.items()
        ]

    @classmethod
    def is_valid_chatbot_type(cls, chatbot_type: str) -> bool:
        if not cls._chatbot_types:
            cls.register_chatbot_types()
        
        return chatbot_type in cls._chatbot_types