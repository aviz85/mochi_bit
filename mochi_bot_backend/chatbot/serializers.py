from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Chatbot, ChatbotSetting, Thread, Message
import logging
from django.conf import settings  # Import the settings module

# Set up logging
logger = logging.getLogger(__name__)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class ChatbotSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatbotSetting
        fields = ['key', 'value']

class ChatbotSerializer(serializers.ModelSerializer):
    settings = serializers.JSONField(write_only=True, required=False)

    class Meta:
        model = Chatbot
        fields = ['id', 'name', 'desc', 'created_at', 'chatbot_type', 'settings', 'visible', 'guest_allowed']
        read_only_fields = ['id', 'created_at', 'owner']

    def create(self, validated_data):
        settings_data = validated_data.pop('settings', {})
        chatbot_type = validated_data.get('chatbot_type')
        default_settings = {
            key: value['default'] 
            for key, value in settings.CHATBOT_TYPES[chatbot_type]['settings'].items()
        }
        # Merge default settings with provided settings
        merged_settings = {**default_settings, **settings_data}

        chatbot = Chatbot.objects.create(**validated_data)
        for key, value in merged_settings.items():
            ChatbotSetting.objects.create(chatbot=chatbot, key=key, value=value)
        return chatbot

    def update(self, instance, validated_data):
        settings_data = validated_data.pop('settings', {})
        instance = super().update(instance, validated_data)
        for key, value in settings_data.items():
            setting, created = ChatbotSetting.objects.get_or_create(chatbot=instance, key=key)
            setting.value = value
            setting.save()
        return instance

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