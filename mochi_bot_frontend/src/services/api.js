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
    return response;
  } catch (error) {
    if (error.response && error.response.status === 404) {
      // If the endpoint doesn't exist, return an empty array
      return { data: [] };
    }
    throw error;
  }
};

export const getChatbotSettings = (chatbotId) => 
  api.get(`/chatbot/${chatbotId}/settings/`);

export const updateChatbotSetting = (chatbotId, key, value) => 
  api.put(`/chatbot/${chatbotId}/setting/${key}/`, { value });

export const deleteChatbotSetting = (chatbotId, key) => 
  api.delete(`/chatbot/${chatbotId}/setting/${key}/`);