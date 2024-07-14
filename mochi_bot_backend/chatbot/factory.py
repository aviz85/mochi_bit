import os
import json
from importlib import import_module

class ChatbotFactory:
    _chatbot_types = {}

    @classmethod
    def register_chatbot_types(cls):
        chatbot_types_dir = os.path.join(os.path.dirname(__file__), 'chatbot_types')
        for type_folder in os.listdir(chatbot_types_dir):
            type_path = os.path.join(chatbot_types_dir, type_folder)
            if os.path.isdir(type_path):
                metadata_path = os.path.join(type_path, 'metadata.json')
                if os.path.exists(metadata_path):
                    with open(metadata_path, 'r') as f:
                        metadata = json.load(f)
                    chatbot_module = import_module(f'.chatbot_types.{type_folder}.chatbot', package='chatbot')
                    chatbot_class = getattr(chatbot_module, f"{metadata['name']}Chatbot")
                    cls._chatbot_types[metadata['type']] = {
                        'class': chatbot_class,
                        'metadata': metadata
                    }

    @classmethod
    def create_chatbot(cls, chatbot_data):
        if not cls._chatbot_types:
            cls.register_chatbot_types()
        
        chatbot_type = chatbot_data['chatbot_type']
        if chatbot_type not in cls._chatbot_types:
            raise ValueError(f"Unknown chatbot type: {chatbot_type}")
        
        return cls._chatbot_types[chatbot_type]['class'](chatbot_data)

    @classmethod
    def get_chatbot_metadata(cls, chatbot_type):
        if not cls._chatbot_types:
            cls.register_chatbot_types()
        
        if chatbot_type not in cls._chatbot_types:
            raise ValueError(f"Unknown chatbot type: {chatbot_type}")
        
        return cls._chatbot_types[chatbot_type]['metadata']

    @classmethod
    def get_all_chatbot_types(cls):
        if not cls._chatbot_types:
            cls.register_chatbot_types()
        
        return [
            {'type': chatbot_type, 'name': info['metadata']['name'], 'description': info['metadata']['description']}
            for chatbot_type, info in cls._chatbot_types.items()
        ]