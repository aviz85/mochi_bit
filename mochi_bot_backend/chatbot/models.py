from django.db import models
from django.contrib.auth.models import User
import uuid
from django.conf import settings

class Chatbot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    desc = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    chatbot_type = models.CharField(max_length=50, choices=[(k, v['name']) for k, v in settings.CHATBOT_TYPES.items()])
    settings = models.JSONField(default=dict)
    visible = models.BooleanField(default=True)
    guest_allowed = models.BooleanField(default=True)

    def get_setting(self, key):
        return self.settings.get(key, settings.CHATBOT_TYPES[self.chatbot_type]['settings'][key]['default'])

    def set_setting(self, key, value):
        self.settings[key] = value
        self.save()

    def generate_response(self, message_content: str, thread_id: str) -> str:
        chatbot_class = ChatbotFactory.get_chatbot_class(self.chatbot_type)
        chatbot_instance = chatbot_class(self.to_dict())
        return chatbot_instance.generate_response(message_content, thread_id)

    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'desc': self.desc,
            'owner_id': str(self.owner.id),
            'created_at': self.created_at.isoformat(),
            'chatbot_type': self.chatbot_type,
            'settings': self.settings,
            'visible': self.visible,
            'guest_allowed': self.guest_allowed,
        }

    def get_setting(self, key):
        return self.settings.get(key, settings.CHATBOT_TYPES[self.chatbot_type]['settings'][key]['default'])

    def set_setting(self, key, value):
        self.settings[key] = value
        self.save()
        
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