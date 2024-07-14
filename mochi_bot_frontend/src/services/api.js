import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const register = (username, email, password) =>
  api.post('/register/', { username, email, password });

export const login = async (username, password) => {
  try {
    console.log('Sending login request:', { username, password });
    const response = await api.post('/login/', { username, password });
    console.log('Login response:', response.data); // Log the response to check its structure
    return response.data; // Ensure the response data is returned
  } catch (error) {
    console.error('Login failed:', error.response);
    throw error;
  }
};

export const logout = () => api.post('/logout/');

export const getChatbots = () => api.get('/chatbot/');

export const createChatbot = (name, chatbot_type, desc = '') =>
  api.post('/chatbot/', { name, chatbot_type, desc });

export const getChatbotTypes = () => api.get('/chatbot_types/');

export const createThread = (chatbot_id) =>
  api.post('/thread/', { chatbot_id });

export const sendMessage = (chatbot_id, thread_id, content) =>
  api.post(`/chatbot/${chatbot_id}/${thread_id}/chat/`, { content });

export const uploadDocument = (chatbot_id, file) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post(`/chatbot/${chatbot_id}/upload_document/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
};

export const deleteDocument = (chatbot_id, document_name) =>
  api.delete(`/chatbot/${chatbot_id}/delete_document/${document_name}/`);

export const getDocuments = (chatbot_id) =>
  api.get(`/chatbot/${chatbot_id}/documents/`);