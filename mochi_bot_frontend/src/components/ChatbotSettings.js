import React, { useState, useEffect, useCallback } from 'react';
import { TextField, Button, Typography, List, ListItem, ListItemText, ListItemSecondaryAction, IconButton } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import { getChatbotSettings, updateChatbotSetting, deleteChatbotSetting } from '../services/api';

function ChatbotSettings({ chatbot }) {
  const [settings, setSettings] = useState([]);
  const [newKey, setNewKey] = useState('');
  const [newValue, setNewValue] = useState('');

  const fetchSettings = useCallback(async () => {
    try {
      const response = await getChatbotSettings(chatbot.id);
      const settingsArray = Array.isArray(response.data) ? response.data : Object.entries(response.data).map(([key, value]) => ({ key, value }));
      setSettings(settingsArray);
    } catch (error) {
      console.error('Failed to fetch settings:', error);
    }
  }, [chatbot.id]);

  useEffect(() => {
    fetchSettings();
  }, [fetchSettings]);

  const handleAddSetting = async () => {
    if (newKey && newValue) {
      try {
        await updateChatbotSetting(chatbot.id, newKey, newValue);
        setNewKey('');
        setNewValue('');
        fetchSettings();
      } catch (error) {
        console.error('Failed to add setting:', error);
      }
    }
  };

  const handleUpdateSetting = async (key, value) => {
    try {
      await updateChatbotSetting(chatbot.id, key, value);
      fetchSettings();
    } catch (error) {
      console.error('Failed to update setting:', error);
    }
  };

  const handleDeleteSetting = async (key) => {
    try {
      await deleteChatbotSetting(chatbot.id, key);
      fetchSettings();
    } catch (error) {
      console.error('Failed to delete setting:', error);
    }
  };

  return (
    <div>
      <Typography variant="h6" gutterBottom>
        Settings for {chatbot.name}
      </Typography>
      <List>
        {settings.map((setting) => (
          <ListItem key={setting.key}>
            <ListItemText
              primary={setting.key}
              secondary={
                <TextField
                  value={setting.value}
                  onChange={(e) => handleUpdateSetting(setting.key, e.target.value)}
                  fullWidth
                />
              }
            />
            <ListItemSecondaryAction>
              <IconButton edge="end" aria-label="delete" onClick={() => handleDeleteSetting(setting.key)}>
                <DeleteIcon />
              </IconButton>
            </ListItemSecondaryAction>
          </ListItem>
        ))}
      </List>
      <Typography variant="subtitle1" gutterBottom>
        Add New Setting
      </Typography>
      <TextField
        label="Key"
        value={newKey}
        onChange={(e) => setNewKey(e.target.value)}
        fullWidth
        margin="normal"
      />
      <TextField
        label="Value"
        value={newValue}
        onChange={(e) => setNewValue(e.target.value)}
        fullWidth
        margin="normal"
      />
      <Button onClick={handleAddSetting} variant="contained" color="primary">
        Add Setting
      </Button>
    </div>
  );
}

export default ChatbotSettings;