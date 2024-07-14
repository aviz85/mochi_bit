from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
import json
from .storage import JSONFileStorage
from .models import User, Chatbot, Thread, Message, UserRole
from .factory import ChatbotFactory
from .file_handler import save_uploaded_file, delete_file, get_file_url
from .serializers import UserSerializer, LoginSerializer

storage = JSONFileStorage('db.json')

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    data = json.loads(request.body)
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    display_name = data.get('display_name', username)
    role = UserRole.USER

    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username already exists'}, status=400)

    user = User.objects.create_user(username=username, email=email, password=password, display_name=display_name, role=role)
    user.save()

    return JsonResponse(UserSerializer(user).data, status=201)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return JsonResponse({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        })
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    request.auth.delete()
    return JsonResponse({}, status=200)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def chatbot_list(request):
    if request.method == 'GET':
        chatbots = Chatbot.objects.all()
        return JsonResponse([chatbot.to_dict() for chatbot in chatbots], safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        chatbot_type = data['chatbot_type']
        
        try:
            metadata = ChatbotFactory.get_chatbot_metadata(chatbot_type)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        
        chatbot = Chatbot(
            name=data['name'],
            desc=data.get('desc', ''),
            owner=request.user,
            chatbot_type=chatbot_type
        )
        chatbot.settings = {k: v['default'] for k, v in metadata['settings_schema'].items()}
        chatbot.save()

        return JsonResponse(chatbot.to_dict(), status=201)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def chatbot_detail(request, chatbot_id):
    try:
        chatbot = Chatbot.objects.get(id=chatbot_id)
    except Chatbot.DoesNotExist:
        return JsonResponse({'error': 'Chatbot not found'}, status=404)

    if request.method == 'GET':
        return JsonResponse(chatbot.to_dict())
    elif request.method == 'PUT':
        data = json.loads(request.body)
        chatbot.name = data.get('name', chatbot.name)
        chatbot.desc = data.get('desc', chatbot.desc)
        chatbot.settings = data.get('settings', chatbot.settings)
        chatbot.save()
        return JsonResponse(chatbot.to_dict())
    elif request.method == 'DELETE':
        chatbot.delete()
        return JsonResponse({}, status=204)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_thread(request):
    data = json.loads(request.body)
    thread = Thread(
        chatbot_id=data['chatbot_id'],
        owner_id=request.user.id
    )
    thread.save()
    return JsonResponse(thread.to_dict(), status=201)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request, chatbot_id, thread_id):
    data = json.loads(request.body)
    content = data['content']

    try:
        chatbot = Chatbot.objects.get(id=chatbot_id)
        thread = Thread.objects.get(id=thread_id)
    except (Chatbot.DoesNotExist, Thread.DoesNotExist):
        return JsonResponse({'error': 'Invalid chatbot or thread'}, status=404)

    user_message = Message(thread=thread, role='user', content=content)
    user_message.save()
    
    response = chatbot.generate_response(content, thread_id)
    
    assistant_message = Message(thread=thread, role='assistant', content=response)
    assistant_message.save()

    return JsonResponse({
        'user_message': user_message.to_dict(),
        'assistant_message': assistant_message.to_dict()
    }, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chatbot_types(request):
    chatbot_types = ChatbotFactory.get_all_chatbot_types()
    return JsonResponse(chatbot_types, safe=False)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_document(request, chatbot_id):
    try:
        chatbot = Chatbot.objects.get(id=chatbot_id)
    except Chatbot.DoesNotExist:
        return JsonResponse({'error': 'Chatbot not found'}, status=404)

    if 'file' not in request.FILES:
        return JsonResponse({'error': 'No file part'}, status=400)
    
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
        return JsonResponse({'message': 'File uploaded successfully', 'file_path': file_path})
    else:
        return JsonResponse({'error': 'File upload failed'}, status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_document(request, chatbot_id, document_name):
    try:
        chatbot = Chatbot.objects.get(id=chatbot_id)
    except Chatbot.DoesNotExist:
        return JsonResponse({'error': 'Chatbot not found'}, status=404)
    documents = chatbot.settings.get('documents', [])
    document = next((doc for doc in documents if doc['name'] == document_name), None)

    if document:
        if delete_file(document['path']):
            documents.remove(document)
            chatbot.settings['documents'] = documents
            chatbot.save()
            return JsonResponse({'message': 'Document deleted successfully'})
        else:
            return JsonResponse({'error': 'Failed to delete document'}, status=500)
    else:
        return JsonResponse({'error': 'Document not found'}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_documents(request, chatbot_id):
    try:
        chatbot = Chatbot.objects.get(id=chatbot_id)
    except Chatbot.DoesNotExist:
        return JsonResponse({'error': 'Chatbot not found'}, status=404)
    documents = chatbot.settings.get('documents', [])

    for doc in documents:
        doc['url'] = get_file_url(doc['path'])

    return JsonResponse({'documents': documents})