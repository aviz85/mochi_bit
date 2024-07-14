// File: src/components/ChatbotSettings.js

import React from 'react';
import { Paper, Typography, TextField, Button } from '@mui/material';

function ChatbotSettings({ chatbot }) {
  const [name, setName] = useState(chatbot.name);
  const [type, setType] = useState(chatbot.chatbot_type);

  const handleSave = () => {
    // Implement save logic here
  };

  return (
    <Paper style={{ padding: '20px', marginTop: '20px' }}>
      <Typography variant="h6" gutterBottom>
        Settings for {chatbot.name}
      </Typography>
      <TextField
        label="Chatbot Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        fullWidth
        margin="normal"
      />
      <TextField
        label="Chatbot Type"
        value={type}
        onChange={(e) => setType(e.target.value)}
        fullWidth
        margin="normal"
      />
      <Button onClick={handleSave} variant="contained" color="primary" fullWidth style={{ marginTop: '10px' }}>
        Save
      </Button>
    </Paper>
  );
}

export default ChatbotSettings;