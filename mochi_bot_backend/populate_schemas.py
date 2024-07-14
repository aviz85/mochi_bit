import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mochi_bot_backend.settings')
django.setup()

from chatbot.models import ChatbotSettingsSchema

# Example schemas
schemas = [
    {
        'chatbot_type': 'echo',
        'schema': {
            'echo_prefix': {
                'type': 'string',
                'default': 'Echo: ',
                'description': 'Prefix to add before echoing the message'
            }
        }
    },
    {
        'chatbot_type': 'claudie',
        'schema': {
            'character': {
                'type': 'string',
                'default': 'You are a helpful AI assistant.',
                'description': 'The character or system prompt for the chatbot'
            },
            'temperature': {
                'type': 'number',
                'default': 1.0,
                'description': 'The temperature setting for the chatbot response, from 0 to 1.',
                'minimum': 0,
                'maximum': 1
            }
        }
    }
    # Add other chatbot types and their schemas here
]

for schema_data in schemas:
    ChatbotSettingsSchema.objects.update_or_create(
        chatbot_type=schema_data['chatbot_type'],
        defaults={'schema': schema_data['schema']}
    )

print("ChatbotSettingsSchema entries created successfully.")