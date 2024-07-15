from django.core.management.base import BaseCommand
from chatbot.models import ChatbotSettingsSchema
from django.conf import settings

class Command(BaseCommand):
    help = 'Initialize chatbot settings schemas'

    def handle(self, *args, **options):
        chatbot_types = getattr(settings, 'CHATBOT_TYPES', {})

        for chatbot_type, config in chatbot_types.items():
            schema = {}
            for setting_name, setting_config in config['settings'].items():
                schema[setting_name] = {
                    'type': setting_config['type'],
                    'default_value': setting_config['default'],
                    'display_name': setting_config.get('display_name', setting_name.replace('_', ' ').title()),
                    'description': setting_config['description'],
                    'required': setting_config.get('required', False)
                }
                
                # Add min and max if they exist for number type
                if setting_config['type'] == 'number':
                    if 'minimum' in setting_config:
                        schema[setting_name]['minimum'] = setting_config['minimum']
                    if 'maximum' in setting_config:
                        schema[setting_name]['maximum'] = setting_config['maximum']

            ChatbotSettingsSchema.objects.update_or_create(
                chatbot_type=chatbot_type,
                defaults={'schema': schema}
            )

            self.stdout.write(self.style.SUCCESS(f'Successfully initialized/updated schema for {chatbot_type}'))

        self.stdout.write(self.style.SUCCESS('All chatbot settings schemas have been initialized/updated.'))