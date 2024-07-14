import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { getChatbots, createChatbot, getChatbotTypes } from '../services/api';
import ChatbotList from './ChatbotList';
import ChatWindow from './ChatWindow';
import { Container, Grid, Typography, Button } from '@mui/material';

function Dashboard() {
  const [chatbots, setChatbots] = useState([]);
  const [chatbotTypes, setChatbotTypes] = useState([]);
  const [selectedChatbot, setSelectedChatbot] = useState(null);
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

  const handleLogout = () => {
    logout();
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
          />
        </Grid>
        <Grid item xs={12} md={8}>
          {selectedChatbot && <ChatWindow chatbot={selectedChatbot} />}
        </Grid>
      </Grid>
    </Container>
  );
}

export default Dashboard;