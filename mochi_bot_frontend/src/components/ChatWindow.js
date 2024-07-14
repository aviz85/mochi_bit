import React, { useState, useEffect, useCallback } from 'react';
import { createThread, sendMessage } from '../services/api';
import { TextField, Button, Typography, Paper, CircularProgress, Snackbar } from '@mui/material';

function ChatWindow({ chatbot }) {
  const [thread, setThread] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const createNewThread = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await createThread(chatbot.id);
      console.log('New thread created:', response);
      setThread(response);
      setMessages([]);
    } catch (error) {
      console.error('Failed to create thread:', error);
      setError('Failed to create a new thread. Please try again.');
    } finally {
      setLoading(false);
    }
  }, [chatbot.id]);

  useEffect(() => {
    createNewThread();
  }, [createNewThread]);

const handleSendMessage = async () => {
  if (input.trim() && thread) {
    const tempMessage = {
      content: input,
      timestamp: new Date().toISOString(),
      role: 'user',
      temporary: true,
    };
    setMessages((prevMessages) => [...prevMessages, tempMessage]);
    setInput('');
    setLoading(true);
    setError(null);

    try {
      const response = await sendMessage(chatbot.id, thread.id, input);
      setMessages((prevMessages) => [
        ...prevMessages.filter((msg) => !msg.temporary),
        response.user_message,
        response.assistant_message,
      ]);
    } catch (error) {
      setError('Failed to send message. Please try again.');
      setMessages((prevMessages) => prevMessages.filter((msg) => !msg.temporary));
    } finally {
      setLoading(false);
    }
  }
};

  useEffect(() => {
    console.log('Messages state updated:', messages);
  }, [messages]);

  return (
    <div>
      <Typography variant="h6" gutterBottom>
        Chat with {chatbot.name}
      </Typography>
      <Paper style={{ height: '400px', overflowY: 'scroll', padding: '10px', marginBottom: '10px' }}>
        {messages.length === 0 ? (
          <Typography color="textSecondary">No messages yet</Typography>
        ) : (
          messages.map((message, index) => (
            message && message.role && (
              <div key={message.timestamp || index} style={{ marginBottom: '10px', padding: '5px', backgroundColor: message.role === 'user' ? '#e6f7ff' : '#f0f0f0', borderRadius: '5px' }}>
                <strong>{message.role === 'user' ? 'You' : 'Bot'}:</strong> {message.content}
              </div>
            )
          ))
        )}
      </Paper>
      <TextField
        value={input}
        onChange={(e) => setInput(e.target.value)}
        fullWidth
        variant="outlined"
        placeholder="Type your message..."
        disabled={loading || !thread}
      />
      <Button 
        onClick={handleSendMessage} 
        variant="contained" 
        color="primary" 
        fullWidth 
        style={{ marginTop: '10px' }}
        disabled={loading || !thread || !input.trim()}
      >
        {loading ? <CircularProgress size={24} /> : 'Send'}
      </Button>
      <Button 
        onClick={createNewThread} 
        variant="outlined" 
        color="secondary" 
        fullWidth 
        style={{ marginTop: '10px' }}
        disabled={loading}
      >
        {loading ? <CircularProgress size={24} /> : 'New Thread'}
      </Button>
      <Snackbar
        open={!!error}
        autoHideDuration={6000}
        onClose={() => setError(null)}
        message={error}
      />
    </div>
  );
}

export default ChatWindow;