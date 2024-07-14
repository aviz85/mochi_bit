from django.conf import settings
from importlib import import_module

class ChatbotFactory:
    @classmethod
    def register_chatbot_types(cls):
        # This method is now a no-op since we're using settings.CHATBOT_TYPES
        pass

    @classmethod
    def get_chatbot_class(cls, chatbot_type):
        if chatbot_type not in settings.CHATBOT_TYPES:
            raise ValueError(f"Unknown chatbot type: {chatbot_type}")
        
        class_path = settings.CHATBOT_TYPES[chatbot_type]['class']
        module_name, class_name = class_path.rsplit('.', 1)
        module = import_module(module_name)
        return getattr(module, class_name)

    @classmethod
    def create_chatbot(cls, chatbot_data):
        from .models import Chatbot  # Import here to avoid circular import
        
        chatbot_type = chatbot_data.get('chatbot_type')
        if not chatbot_type:
            raise ValueError("chatbot_type is required in chatbot_data")
        
        if chatbot_type not in settings.CHATBOT_TYPES:
            raise ValueError(f"Unknown chatbot type: {chatbot_type}")
        
        chatbot = Chatbot.objects.create(**chatbot_data)
        
        # Set default settings
        default_settings = {
            key: value['default']
            for key, value in settings.CHATBOT_TYPES[chatbot_type]['settings'].items()
        }
        chatbot.settings = default_settings
        chatbot.save()
        
        return chatbot

    @classmethod
    def get_chatbot_metadata(cls, chatbot_type):
        if chatbot_type not in settings.CHATBOT_TYPES:
            raise ValueError(f"Unknown chatbot type: {chatbot_type}")
        
        return settings.CHATBOT_TYPES[chatbot_type]

    @classmethod
    def get_all_chatbot_types(cls):
        return [
            {'type': chatbot_type, 'name': info['name'], 'description': info['description']}
            for chatbot_type, info in settings.CHATBOT_TYPES.items()
        ]

    @classmethod
    def is_valid_chatbot_type(cls, chatbot_type):
        return chatbot_type in settings.CHATBOT_TYPES