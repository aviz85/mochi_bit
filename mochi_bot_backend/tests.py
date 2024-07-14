from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from .models import Chatbot, Thread, Message
import json

class ChatbotAPITests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.chatbot = Chatbot.objects.create(name="Test Chatbot", owner=self.user, chatbot_type="test_type", settings={})
        self.thread = Thread.objects.create(chatbot=self.chatbot, owner=self.user)
        self.client.login(username='testuser', password='password')

    def test_register_user(self):
        url = reverse('register_user')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword'
        }
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_login_user(self):
        url = reverse('login_user')
        data = {
            'username': 'aviz85',
            'password': 'aa9973736m'
        }
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_logout_user(self):
        url = reverse('logout_user')
        response = self.client.post(url, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], 'Successfully logged out.')

    def test_chatbot_list(self):
        url = reverse('chatbot_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_thread(self):
        url = reverse('create_thread')
        data = {'chatbot': self.chatbot.id}
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Thread.objects.count(), 2)

    def test_send_message(self):
        url = reverse('send_message', kwargs={'chatbot_id': self.chatbot.id, 'thread_id': self.thread.id})
        data = {'content': 'Hello!'}
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Message.objects.count(), 2)

    def test_chatbot_detail(self):
        url = reverse('chatbot_detail', kwargs={'chatbot_id': self.chatbot.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.chatbot.id)

    def test_upload_document(self):
        url = reverse('upload_document', kwargs={'chatbot_id': self.chatbot.id})
        with open('testfile.txt', 'w') as f:
            f.write('test content')
        with open('testfile.txt', 'rb') as f:
            response = self.client.post(url, {'file': f})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('file_path', response.data)

    def test_delete_document(self):
        document_name = 'testfile.txt'
        self.chatbot.settings['documents'] = [{'name': document_name, 'path': '/path/to/testfile.txt'}]
        self.chatbot.save()
        url = reverse('delete_document', kwargs={'chatbot_id': self.chatbot.id, 'document_name': document_name})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_documents(self):
        document_name = 'testfile.txt'
        self.chatbot.settings['documents'] = [{'name': document_name, 'path': '/path/to/testfile.txt'}]
        self.chatbot.save()
        url = reverse('get_documents', kwargs={'chatbot_id': self.chatbot.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['documents']), 1)