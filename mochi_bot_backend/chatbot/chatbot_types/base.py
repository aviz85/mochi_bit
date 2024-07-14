from abc import ABC, abstractmethod

class BaseChatbot(ABC):
    def __init__(self, chatbot_data):
        self.id = chatbot_data['id']
        self.name = chatbot_data['name']
        self.settings = chatbot_data['settings']

    @abstractmethod
    def generate_response(self, message_content: str, thread_id: str) -> str:
        pass

    @abstractmethod
    def get_settings_schema(self):
        pass

    @abstractmethod
    def validate_settings(self, settings):
        pass