# management/commands/init_chatbot_schemas.py

from django.core.management.base import BaseCommand
from chatbot.models import ChatbotSettingsSchema

class Command(BaseCommand):
    help = 'Initialize chatbot settings schemas'

    def handle(self, *args, **options):
        schemas = [
            {
                'chatbot_type': 'echo',
                'schema': {
                    'echo_prefix': {
                        'type': 'string',
                        'default_value': 'Echo: ',
                        'display_name': 'Echo Prefix',
                        'description': 'Prefix to add before echoing the message',
                        'required': True
                    }
                }
            },
            {
                'chatbot_type': 'claudie',
                'schema': {
                    'character': {
                        'type': 'string',
                        'default_value': 'You are a helpful AI assistant.',
                        'display_name': 'Character Description',
                        'description': 'The character or system prompt for the chatbot',
                        'required': True
                    },
                    'temperature': {
                        'type': 'number',
                        'default_value': 1.0,
                        'display_name': 'Temperature',
                        'description': 'Controls randomness in the output. Higher values make the output more random.',
                        'required': False
                    }
                }
            }
        ]

        for schema_data in schemas:
            ChatbotSettingsSchema.objects.update_or_create(
                chatbot_type=schema_data['chatbot_type'],
                defaults={'schema': schema_data['schema']}
            )

        self.stdout.write(self.style.SUCCESS('Successfully initialized chatbot settings schemas'))