import React, { useState, useEffect } from 'react';
import ChatbotList from './ChatbotList'; // Ensure this import path is correct
import { getChatbots, getChatbotTypes, createChatbot, deleteChatbot } from '../services/api'; // Ensure these API functions are correctly imported

function ChatbotManager() {
  const [chatbots, setChatbots] = useState([]);
  const [chatbotTypes, setChatbotTypes] = useState([]);
  const [selectedChatbot, setSelectedChatbot] = useState(null);

  useEffect(() => {
    fetchChatbots();
    fetchChatbotTypes();
  }, []);

  const fetchChatbots = async () => {
    try {
      const response = await getChatbots();
      setChatbots(response.data);
    } catch (error) {
      console.error('Failed to fetch chatbots:', error);
    }
  };

  const fetchChatbotTypes = async () => {
    try {
      const response = await getChatbotTypes();
      setChatbotTypes(response.data);
    } catch (error) {
      console.error('Failed to fetch chatbot types:', error);
    }
  };

  const handleCreateChatbot = async (name, type) => {
    try {
      await createChatbot(name, type);
      fetchChatbots();
    } catch (error) {
      console.error('Failed to create chatbot:', error);
    }
  };

  const handleDeleteChatbot = async (id) => {
    try {
      await deleteChatbot(id);
      fetchChatbots();
    } catch (error) {
      console.error('Failed to delete chatbot:', error);
    }
  };

  const handleSelectChatbot = (chatbot) => {
    setSelectedChatbot(chatbot);
  };

  return (
    <div>
      <ChatbotList
        chatbots={chatbots}
        chatbotTypes={chatbotTypes}
        onCreateChatbot={handleCreateChatbot}
        onSelectChatbot={handleSelectChatbot}
        onDeleteChatbot={handleDeleteChatbot}
      />
      {selectedChatbot && (
        <div>
          <h2>Selected Chatbot: {selectedChatbot.name}</h2>
          {/* Add more details or actions for the selected chatbot here */}
        </div>
      )}
    </div>
  );
}

export default ChatbotManager;