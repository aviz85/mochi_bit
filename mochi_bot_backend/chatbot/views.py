import logging
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import User, Chatbot, Thread, Message, ChatbotSettingsSchema
from .serializers import UserSerializer, LoginSerializer, ChatbotSerializer, ThreadSerializer, MessageSerializer
from .factory import ChatbotFactory
from .file_handler import save_uploaded_file, delete_file, get_file_url
logger = logging.getLogger(__name__)
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json  # Add this import
from django.middleware.csrf import get_token
from django.db.models import Count
from rest_framework.exceptions import ValidationError

@csrf_exempt
def debug_view(request):
    csrf_token = get_token(request)
    headers = request.headers
    print(f"CSRF Token: {csrf_token}")
    print(f"Headers: {headers}")
    return JsonResponse({'csrf_token': csrf_token, 'headers': dict(headers)})
    
class ChatbotViewSet(viewsets.ModelViewSet):
    queryset = Chatbot.objects.all()
    serializer_class = ChatbotSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chat_logs(request, chatbot_id):
    chatbot = get_object_or_404(Chatbot, id=chatbot_id, owner=request.user)
    threads = Thread.objects.filter(chatbot=chatbot, visible=True).annotate(
        message_count=Count('message')
    ).filter(message_count__gt=0)
    
    logs = []
    for thread in threads:
        messages = Message.objects.filter(thread=thread).order_by('created_at')
        thread_data = {
            'thread_id': thread.id,
            'created_at': thread.created_at,
            'messages': MessageSerializer(messages, many=True).data
        }
        logs.append(thread_data)
    
    return Response(logs)
     
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def chatbot_settings(request, chatbot_id):
    chatbot = get_object_or_404(Chatbot, id=chatbot_id)

    # Debugging prints
    print(f"Request user: {request.user}")
    print(f"Chatbot owner: {chatbot.owner}")
    print(f"Is admin: {request.user.is_staff}")
    print(f"Request headers: {request.headers}")

    # Check if the request user is the owner of the chatbot or an admin
    if not (request.user == chatbot.owner or request.user.is_staff):
        return Response({'error': 'Permission denied'}, status=403)

    schema = ChatbotSettingsSchema.objects.get(chatbot_type=chatbot.chatbot_type)

    if request.method == "GET":
        settings = {}
        for key, setting_schema in schema.schema.items():
            setting_value = chatbot.settings.get(key, setting_schema['default'])
            settings[key] = {
                'value': setting_value,
                'display_name': setting_schema.get('display_name', key),
                'description': setting_schema.get('description', ''),
                'type': setting_schema['type'],
                'default_value': setting_schema['default'],
                'required': setting_schema.get('required', False)
            }
        return Response(settings)

    elif request.method == "PUT":
        try:
            settings_data = json.loads(request.body)
            for key, value in settings_data.items():
                if key not in schema.schema:
                    raise ValidationError(f"Invalid setting: {key}")
                schema.validate_setting(key, value)
                chatbot.settings[key] = value
            chatbot.save()  # Save the updated settings
            
            # Return the full updated settings
            updated_settings = {}
            for key, setting_schema in schema.schema.items():
                setting_value = chatbot.settings.get(key, setting_schema['default'])
                updated_settings[key] = {
                    'value': setting_value,
                    'display_name': setting_schema.get('display_name', key),
                    'description': setting_schema.get('description', ''),
                    'type': setting_schema['type'],
                    'default_value': setting_schema['default'],
                    'required': setting_schema.get('required', False)
                }
            return Response(updated_settings)
        except json.JSONDecodeError:
            return Response({'error': 'Invalid JSON'}, status=400)
        except ValidationError as e:
            return Response({'error': str(e)}, status=400)
            
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
            password=request.data['password']
        )
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    try:
        request.user.auth_token.delete()
    except (AttributeError, User.auth_token.RelatedObjectDoesNotExist):
        pass
    return Response({"success": "Successfully logged out."}, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def chatbot_list(request):
    print(f"Request user: {request.user}")

    if request.method == 'GET':
        chatbots = Chatbot.objects.filter(owner=request.user)
        serializer = ChatbotSerializer(chatbots, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        chatbot_type = request.data.get('chatbot_type')
        if not chatbot_type:
            return Response({'error': 'Chatbot type is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            chatbot_metadata = ChatbotFactory.get_chatbot_metadata(chatbot_type)
            logger.info(f"Chatbot metadata for type {chatbot_type}: {chatbot_metadata}")
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        # Ensure 'settings' exists in chatbot_metadata
        settings = chatbot_metadata.get('settings')
        if settings is None:
            return Response({'error': 'Invalid chatbot metadata: missing settings'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ChatbotSerializer(data=request.data)
        if serializer.is_valid():
            # Initialize settings with default values
            initialized_settings = {k: v.get('default', '') for k, v in settings.items()}
            logger.info(f"Initial settings: {initialized_settings}")
            
            # Update settings with provided values if any
            if 'settings' in request.data:
                initialized_settings.update(request.data['settings'])
                logger.info(f"Updated settings: {initialized_settings}")
            
            chatbot = serializer.save(owner=request.user, chatbot_type=chatbot_type, settings=initialized_settings)
            return Response(ChatbotSerializer(chatbot).data, status=status.HTTP_201_CREATED)
        
        logger.error(f"Chatbot creation failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def chatbot_detail(request, chatbot_id):
    chatbot = get_object_or_404(Chatbot, id=chatbot_id, owner=request.user)

    if request.method == 'GET':
        serializer = ChatbotSerializer(chatbot)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ChatbotSerializer(chatbot, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        chatbot.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_thread(request):
    print(f"Request user: {request.user}")

    logger.info(f"Received data for thread creation: {request.data}")
    
    chatbot_id = request.data.get('chatbot')
    if not chatbot_id:
        logger.error("No chatbot ID provided")
        return Response({'error': 'Chatbot ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        chatbot = Chatbot.objects.get(id=chatbot_id, owner=request.user)
    except Chatbot.DoesNotExist:
        logger.error(f"Chatbot with id {chatbot_id} not found or doesn't belong to the user")
        return Response({'error': 'Invalid chatbot ID'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = ThreadSerializer(data={'chatbot': chatbot.id}, context={'request': request})
    if serializer.is_valid():
        thread = serializer.save(owner=request.user)
        logger.info(f"Thread created successfully: {thread.id}")
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    logger.error(f"Thread creation failed. Errors: {serializer.errors}")
    return Response({
        'error': 'Invalid data',
        'details': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    try:
        # Log the incoming request data
        logger.debug(f"Request data: {request.data}")

        # Extract necessary fields from the request data
        chatbot_id = request.data.get('chatbot_id')
        thread_id = request.data.get('thread_id')
        content = request.data.get('content')

        # Validate that all required fields are present
        if not chatbot_id or not thread_id or not content:
            return Response({'error': 'chatbot_id, thread_id, and content are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the chatbot and thread objects
        chatbot = get_object_or_404(Chatbot, id=chatbot_id)
        thread = get_object_or_404(Thread, id=thread_id)

        # Serialize and save the user message
        user_message_serializer = MessageSerializer(data={'thread': thread.id, 'role': 'user', 'content': content})
        if user_message_serializer.is_valid():
            user_message = user_message_serializer.save()
        else:
            logger.error(f"User message serializer errors: {user_message_serializer.errors}")
            return Response(user_message_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Generate the response from the chatbot
        response = chatbot.generate_response(content, thread_id)

        # Serialize and save the assistant message
        assistant_message_serializer = MessageSerializer(data={'thread': thread.id, 'role': 'assistant', 'content': response})
        if assistant_message_serializer.is_valid():
            assistant_message = assistant_message_serializer.save()
        else:
            logger.error(f"Assistant message serializer errors: {assistant_message_serializer.errors}")
            return Response(assistant_message_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Return the user and assistant messages
        return Response({
            'user_message': MessageSerializer(user_message).data,
            'assistant_message': MessageSerializer(assistant_message).data
        }, status=status.HTTP_200_OK)
    except Exception as e:
        logger.exception("An error occurred in send_message")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chatbot_types(request):
    chatbot_types = ChatbotFactory.get_all_chatbot_types()
    return Response(chatbot_types)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_document(request, chatbot_id):
    chatbot = get_object_or_404(Chatbot, id=chatbot_id, owner=request.user)

    if 'file' not in request.FILES:
        return Response({'error': 'No file part'}, status=status.HTTP_400_BAD_REQUEST)
    
    file = request.FILES['file']
    file_path = save_uploaded_file(file)
    
    if file_path:
        if 'documents' not in chatbot.settings:
            chatbot.settings['documents'] = []
        chatbot.settings['documents'].append({
            'name': file.name,
            'path': file_path
        })
        chatbot.save()
        return Response({'message': 'File uploaded successfully', 'file_path': file_path})
    else:
        return Response({'error': 'File upload failed'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_document(request, chatbot_id, document_name):
    chatbot = get_object_or_404(Chatbot, id=chatbot_id, owner=request.user)
    documents = chatbot.settings.get('documents', [])
    document = next((doc for doc in documents if doc['name'] == document_name), None)

    if document:
        if delete_file(document['path']):
            documents.remove(document)
            chatbot.settings['documents'] = documents
            chatbot.save()
            return Response({'message': 'Document deleted successfully'})
        else:
            return Response({'error': 'Failed to delete document'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_documents(request, chatbot_id):
    chatbot = get_object_or_404(Chatbot, id=chatbot_id, owner=request.user)
    documents = chatbot.settings.get('documents', [])

    for doc in documents:
        doc['url'] = get_file_url(doc['path'])

    return Response({'documents': documents})
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id, owner=request.user)

    if request.method == 'GET':
        serializer = ThreadSerializer(thread)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ThreadSerializer(thread, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        thread.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)