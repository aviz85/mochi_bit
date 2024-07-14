from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from chatbot import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', views.register_user),
    path('api/login/', views.login_user),
    path('api/logout/', views.logout_user),
    path('api/chatbot/', views.chatbot_list),
    path('api/chatbot/<str:chatbot_id>/', views.chatbot_detail),
    path('api/thread/', views.create_thread),
    path('api/chat/', views.send_message),
    path('api/chatbot_types/', views.get_chatbot_types),
    path('api/chatbot/<str:chatbot_id>/upload_document/', views.upload_document),
    path('api/chatbot/<str:chatbot_id>/delete_document/<str:document_name>/', views.delete_document),
    path('api/chatbot/<str:chatbot_id>/documents/', views.get_documents),
    path('api/chatbot/<str:chatbot_id>/settings/', views.chatbot_settings),
    path('api/chatbot/<str:chatbot_id>/setting/<str:key>/', views.chatbot_setting)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)