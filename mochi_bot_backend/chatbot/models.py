from django.db import models
from django.contrib.auth.models import User
import uuid
from django.conf import settings
from importlib import import_module  # Import import_module
from django.core.exceptions import ValidationError

class ChatbotSettingsSchema(models.Model):
    chatbot_type = models.CharField(max_length=50, unique=True)
    schema = models.JSONField()

    def convert_value(self, key, value):
        if key not in self.schema:
            return value
        
        setting_type = self.schema[key]['type']
        if setting_type == 'number':
            try:
                return float(value)
            except (ValueError, TypeError):
                return self.schema[key]['default']
        elif setting_type == 'string':
            return str(value)
        elif setting_type == 'boolean':
            return bool(value)
        return value

    def validate_setting(self, key, value):
        if key not in self.schema:
            raise ValidationError(f"Unknown setting '{key}' for chatbot type '{self.chatbot_type}'")
        
        schema_setting = self.schema[key]
        converted_value = self.convert_value(key, value)
        
        if schema_setting['type'] == 'number':
            if not isinstance(converted_value, (int, float)):
                raise ValidationError(f"Setting '{key}' must be a number")
            if 'minimum' in schema_setting and converted_value < schema_setting['minimum']:
                raise ValidationError(f"Setting '{key}' must be at least {schema_setting['minimum']}")
            if 'maximum' in schema_setting and converted_value > schema_setting['maximum']:
                raise ValidationError(f"Setting '{key}' must be at most {schema_setting['maximum']}")
        elif schema_setting['type'] == 'string' and not isinstance(converted_value, str):
            raise ValidationError(f"Setting '{key}' must be a string")
        elif schema_setting['type'] == 'boolean' and not isinstance(converted_value, bool):
            raise ValidationError(f"Setting '{key}' must be a boolean")   
            
class ChatbotSettingsDict:
    def __init__(self, chatbot):
        self.chatbot = chatbot

    def get(self, key, default=None):
        try:
            setting = ChatbotSetting.objects.get(chatbot=self.chatbot, key=key)
            return setting.get_value()
        except ChatbotSetting.DoesNotExist:
            return default

    def __getitem__(self, key):
        value = self.get(key)
        if value is None:
            raise KeyError(key)
        return value

    def __setitem__(self, key, value):
        setting, created = ChatbotSetting.objects.get_or_create(chatbot=self.chatbot, key=key)
        setting.set_value(value)
        setting.save()

class Chatbot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    desc = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    chatbot_type = models.CharField(max_length=50)
    visible = models.BooleanField(default=True)
    guest_allowed = models.BooleanField(default=True)

    @property
    def settings(self):
        return ChatbotSettingsDict(self)

    def get_setting(self, key, default=None):
        return self.settings.get(key, default)


    def generate_response(self, message_content: str, thread_id: str) -> str:
        chatbot_class = self.get_chatbot_class()
        chatbot_instance = chatbot_class(self.to_dict())
        return chatbot_instance.generate_response(message_content, thread_id)

    def get_chatbot_class(self):
        chatbot_type = self.chatbot_type
        class_path = settings.CHATBOT_TYPES[chatbot_type]['class']
        module_name, class_name = class_path.rsplit('.', 1)
        module = import_module(module_name)
        return getattr(module, class_name)
        
    @property
    def settings(self):
        return ChatbotSettingsDict(self)

    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'desc': self.desc,
            'owner_id': str(self.owner.id),
            'created_at': self.created_at.isoformat(),
            'chatbot_type': self.chatbot_type,
            'settings': {setting.key: setting.value for setting in self.chatbot_settings.all()},
            'visible': self.visible,
            'guest_allowed': self.guest_allowed,
        }
        
class ChatbotSetting(models.Model):
    chatbot = models.ForeignKey(Chatbot, related_name='chatbot_settings', on_delete=models.CASCADE)
    key = models.CharField(max_length=100)
    value = models.JSONField()

    class Meta:
        unique_together = ('chatbot', 'key')

    def get_value(self):
        schema = ChatbotSettingsSchema.objects.get(chatbot_type=self.chatbot.chatbot_type)
        return schema.convert_value(self.key, self.value)

    def set_value(self, new_value):
        schema = ChatbotSettingsSchema.objects.get(chatbot_type=self.chatbot.chatbot_type)
        self.value = schema.convert_value(self.key, new_value)


class Thread(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chatbot = models.ForeignKey(Chatbot, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict)
    visible = models.BooleanField(default=True)

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict)
    visible = models.BooleanField(default=True)