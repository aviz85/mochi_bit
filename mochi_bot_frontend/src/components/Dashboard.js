import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { getChatbots, createChatbot, getChatbotTypes, deleteChatbot } from '../services/api';
import ChatbotList from './ChatbotList';
import ChatWindow from './ChatWindow';
import ChatbotSettings from './ChatbotSettings';
import { Container, Grid, Typography, Button, Tabs, Tab } from '@mui/material';

function Dashboard() {
  const [chatbots, setChatbots] = useState([]);
  const [chatbotTypes, setChatbotTypes] = useState([]);
  const [selectedChatbot, setSelectedChatbot] = useState(null);
  const [activeTab, setActiveTab] = useState(0);
  const { logout } = useAuth();

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
      const response = await createChatbot(name, type);
      setChatbots([...chatbots, response.data]);
    } catch (error) {
      console.error('Failed to create chatbot:', error);
    }
  };

  const handleDeleteChatbot = async (id) => {
    try {
      await deleteChatbot(id);
      setChatbots(chatbots.filter(chatbot => chatbot.id !== id));
      if (selectedChatbot && selectedChatbot.id === id) {
        setSelectedChatbot(null);
        setActiveTab(0);
      }
    } catch (error) {
      console.error('Failed to delete chatbot:', error);
    }
  };

  const handleLogout = () => {
    logout();
  };

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  return (
    <Container>
      <Typography variant="h4" component="h1" gutterBottom>
        Dashboard
      </Typography>
      <Button onClick={handleLogout} variant="contained" color="secondary">
        Logout
      </Button>
      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <ChatbotList
            chatbots={chatbots}
            chatbotTypes={chatbotTypes}
            onCreateChatbot={handleCreateChatbot}
            onSelectChatbot={setSelectedChatbot}
            onDeleteChatbot={handleDeleteChatbot}
          />
        </Grid>
        <Grid item xs={12} md={8}>
          {selectedChatbot && (
            <>
              <Tabs value={activeTab} onChange={handleTabChange}>
                <Tab label="Chat" />
                <Tab label="Settings" />
              </Tabs>
              {activeTab === 0 && <ChatWindow chatbot={selectedChatbot} />}
              {activeTab === 1 && <ChatbotSettings chatbot={selectedChatbot} />}
            </>
          )}
        </Grid>
      </Grid>
    </Container>
  );
}

export default Dashboard;