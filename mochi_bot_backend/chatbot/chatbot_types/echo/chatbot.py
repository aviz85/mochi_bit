from ..base import BaseChatbot

class EchoChatbot(BaseChatbot):
    def generate_response(self, message_content: str, thread_id: str) -> str:
        prefix = self.settings.get('echo_prefix', 'Echo: ')
        return f"{prefix}{message_content}"

    def get_settings_schema(self):
        return {
            "echo_prefix": {
                "type": "string",
                "default": "Echo: ",
                "description": "Prefix to add before echoing the message"
            }
        }

    def validate_settings(self, settings):
        if 'echo_prefix' in settings and not isinstance(settings['echo_prefix'], str):
            raise ValueError("echo_prefix must be a string")
        return settings