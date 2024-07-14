from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Chatbot, Thread, Message
import logging

# Set up logging
logger = logging.getLogger(__name__)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class ChatbotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chatbot
        fields = ['id', 'name', 'desc', 'created_at', 'chatbot_type', 'settings', 'visible', 'guest_allowed']
        read_only_fields = ['id', 'created_at', 'owner']

class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = ['id', 'chatbot', 'owner', 'created_at', 'metadata', 'visible']
        read_only_fields = ['id', 'created_at', 'owner']

class MessageSerializer(serializers.ModelSerializer):
    thread = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Thread.objects.all()
    )  # Use ID for validation and creation

    class Meta:
        model = Message
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['thread'] = ThreadSerializer(instance.thread).data  # Serialize thread as object
        return rep

    def validate(self, data):
        logger.debug(f"Validating message data: {data}")
        return data
          
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        logger.debug(f"Validating login data: {data}")
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                data['user'] = user
            else:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")
        return data