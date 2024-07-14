# File: mochi_bot_backend/urls.py

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from chatbot import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication
    path('api/register/', views.register_user, name='register'),
    path('api/login/', views.login_user, name='login'),
    path('api/logout/', views.logout_user, name='logout'),
    
    # Chatbot operations
    path('api/chatbot/', views.chatbot_list, name='chatbot-list'),
    path('api/chatbot/<str:chatbot_id>/', views.chatbot_detail, name='chatbot-detail'),
    path('api/chatbot/<str:chatbot_id>/upload_document/', views.upload_document, name='upload-document'),
    path('api/chatbot/<str:chatbot_id>/delete_document/<str:document_name>/', views.delete_document, name='delete-document'),
    path('api/chatbot/<str:chatbot_id>/documents/', views.get_documents, name='get-documents'),
    path('api/chatbot_types/', views.get_chatbot_types, name='chatbot-types'),
    
    # Thread operations
    path('api/thread/', views.create_thread, name='create-thread'),
    path('api/chatbot/<str:chatbot_id>/<str:thread_id>/chat/', views.send_message, name='send-message'),
    path('api/thread/<str:thread_id>/', views.thread_detail, name='thread-detail'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)