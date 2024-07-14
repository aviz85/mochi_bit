import React, { useState, useEffect, useCallback } from 'react';
import { createThread, sendMessage } from '../services/api';
import { TextField, Button, Typography, Paper } from '@mui/material';

function ChatWindow({ chatbot }) {
  const [thread, setThread] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const createNewThread = useCallback(async () => {
    try {
      const response = await createThread(chatbot.id);
      setThread(response.data);
      setMessages([]);
    } catch (error) {
      console.error('Failed to create thread:', error);
    }
  }, [chatbot.id]);

  useEffect(() => {
    createNewThread();
  }, [createNewThread]);

  const handleSendMessage = async () => {
    if (input.trim() && thread) {
      try {
        const response = await sendMessage(chatbot.id, thread.id, input);
        setMessages([...messages, response.data.user_message, response.data.assistant_message]);
        setInput('');
      } catch (error) {
        console.error('Failed to send message:', error);
      }
    }
  };

  return (
    <div>
      <Typography variant="h6" gutterBottom>
        Chat with {chatbot.name}
      </Typography>
      <Paper style={{ height: '400px', overflowY: 'scroll', padding: '10px', marginBottom: '10px' }}>
        {messages.map((message, index) => (
          <div key={index} style={{ marginBottom: '10px' }}>
            <strong>{message.role}:</strong> {message.content}
          </div>
        ))}
      </Paper>
      <TextField
        value={input}
        onChange={(e) => setInput(e.target.value)}
        fullWidth
        variant="outlined"
        placeholder="Type your message..."
      />
      <Button onClick={handleSendMessage} variant="contained" color="primary" fullWidth style={{ marginTop: '10px' }}>
        Send
      </Button>
      <Button onClick={createNewThread} variant="outlined" color="secondary" fullWidth style={{ marginTop: '10px' }}>
        New Thread
      </Button>
    </div>
  );
}

export default ChatWindow;