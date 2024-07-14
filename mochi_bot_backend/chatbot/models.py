from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from enum import Enum

class UserRole(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    MANAGER = 'manager', 'Manager'
    USER = 'user', 'User'

class User(AbstractUser):
    display_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=UserRole.choices, default=UserRole.USER)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Change this to avoid conflict
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',  # Change this to avoid conflict
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def to_dict(self):
        return {
            'id': str(self.id),
            'username': self.username,
            'display_name': self.display_name,
            'email': self.email,
            'role': self.role,
        }

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

class Thread(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chatbot = models.ForeignKey(Chatbot, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict)
    visible = models.BooleanField(default=True)

    def to_dict(self):
        return {
            'id': str(self.id),
            'chatbot_id': str(self.chatbot.id),
            'owner_id': str(self.owner.id) if self.owner else None,
            'created_at': self.created_at.isoformat(),
            'metadata': self.metadata,
            'visible': self.visible,
        }

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict)
    visible = models.BooleanField(default=True)

    def to_dict(self):
        return {
            'id': str(self.id),
            'thread_id': str(self.thread.id),
            'role': self.role,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'metadata': self.metadata,
            'visible': self.visible,
        }