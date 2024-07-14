from django.db import models
from django.contrib.auth.models import User
import uuid
from .factory import ChatbotFactory


class Chatbot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    desc = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    chatbot_type = models.CharField(max_length=50)
    settings = models.JSONField(default=dict)
    visible = models.BooleanField(default=True)
    guest_allowed = models.BooleanField(default=True)

    def generate_response(self, content, thread_id):
        chatbot_instance = ChatbotFactory.create_chatbot({
            'id': str(self.id),
            'name': self.name,
            'chatbot_type': self.chatbot_type,
            'settings': self.settings
        })
        return chatbot_instance.generate_response(content, thread_id)

    def __str__(self):
        return self.name
        
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