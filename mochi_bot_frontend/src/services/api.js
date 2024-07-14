import axios from 'axios';
import Cookies from 'js-cookie';

const API_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  const csrfToken = Cookies.get('csrftoken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  if (csrfToken) {
    config.headers['X-CSRFToken'] = csrfToken;
  }
  return config;
});

export const getChatbotSettings = async (chatbotId) => {
  console.log('Fetching settings for chatbotId:', chatbotId);
  try {
    const response = await api.get(`/chatbot/${chatbotId}/settings/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching chatbot settings:', error);
    throw error;
  }
};

export const updateChatbotSettings = async (chatbotId, settings) => {
  try {
    const response = await api.put(`/chatbot/${chatbotId}/settings/`, settings);
    return response.data;
  } catch (error) {
    console.error('Error updating chatbot settings:', error);
    throw error;
  }
};

export const debugRequest = async () => {
  try {
    const response = await api.get('/debug/', { withCredentials: true });
    console.log('Debug Response:', response.data);
  } catch (error) {
    console.error('Debug Request Error:', error.response?.data || error.message);
  }
};

export const register = (username, email, password) => 
  api.post('/register/', { username, email, password });

export const login = async (username, password) => {
  try {
    console.log('Sending login request:', { username, password });
    const response = await api.post('/login/', { username, password });
    console.log('Login response:', response.data);
    return response.data;
  } catch (error) {
    console.error('Login failed:', error.response?.data || error.message);
    throw error;
  }
};

export const logout = () => api.post('/logout/');

export const getChatbots = () => api.get('/chatbot/');

export const createChatbot = (name, chatbot_type, desc = '') => 
  api.post('/chatbot/', { name, chatbot_type, desc });

export const deleteChatbot = (id) => api.delete(`/chatbot/${id}/`);

export const getChatbotTypes = () => api.get('/chatbot_types/');

export const createThread = async (chatbotId) => {
  try {
    console.log('Creating thread for chatbot:', chatbotId);
    const response = await api.post('/thread/', { chatbot: chatbotId });
    console.log('Thread created successfully:', response.data);
    return response.data;
  } catch (error) {
    console.error('Failed to create thread:', error.response?.data || error.message);
    throw error;
  }
};

export const sendMessage = async (chatbotId, threadId, content) => {
  try {
    console.log('Sending message:', { chatbotId, threadId, content });
    const response = await api.post('/chat/', { chatbot_id: chatbotId, thread_id: threadId, content });
    console.log('sendMessage response:', response.data);
    return response.data;
  } catch (error) {
    console.error('sendMessage error:', error.response?.data || error.message);
    throw error;
  }
};

export const uploadDocument = (chatbotId, file) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post(`/chatbot/${chatbotId}/upload_document/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const deleteDocument = (chatbotId, documentName) => 
  api.delete(`/chatbot/${chatbotId}/delete_document/${documentName}/`);

export const getDocuments = (chatbotId) => 
  api.get(`/chatbot/${chatbotId}/documents/`);

export const getChatLogs = async (chatbotId) => {
  try {
    const response = await api.get(`/chatbot/${chatbotId}/logs/`);
    return response.data;
  } catch (error) {
    console.error('Failed to fetch chat logs:', error);
    throw error;
  }
};