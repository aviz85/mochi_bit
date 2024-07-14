import React, { useState, useEffect, useCallback } from 'react';
import { TextField, Button, Typography, List, ListItem, ListItemText, ListItemSecondaryAction, IconButton, Slider, Select, MenuItem, FormControl, InputLabel } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import { getChatbotSettings, updateChatbotSetting, deleteChatbotSetting } from '../services/api';

function ChatbotSettings({ chatbot }) {
  const [settings, setSettings] = useState([]);
  const [newKey, setNewKey] = useState('');
  const [newValue, setNewValue] = useState('');
  const [newType, setNewType] = useState('string'); // Default type for new settings

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
        const newSettings = [...settings, { key: newKey, value: newValue, type: newType }];
        setSettings(newSettings);
        setNewKey('');
        setNewValue('');
        setNewType('string');
      } catch (error) {
        console.error('Failed to add setting:', error);
      }
    }
  };

  const handleUpdateSetting = (key, value) => {
    const updatedSettings = settings.map((setting) =>
      setting.key === key ? { ...setting, value } : setting
    );
    setSettings(updatedSettings);
  };

  const handleDeleteSetting = async (key) => {
    try {
      await deleteChatbotSetting(chatbot.id, key);
      fetchSettings();
    } catch (error) {
      console.error('Failed to delete setting:', error);
    }
  };

  const handleSaveSettings = async () => {
    try {
      for (const setting of settings) {
        await updateChatbotSetting(chatbot.id, setting.key, setting.value);
      }
      fetchSettings();
    } catch (error) {
      console.error('Failed to save settings:', error);
    }
  };

  const renderWidget = (setting) => {
    switch (setting.type) {
      case 'number':
        return (
          <Slider
            value={Number(setting.value)}
            onChange={(e, newValue) => handleUpdateSetting(setting.key, newValue)}
            min={0}
            max={1}
            step={0.01}
            marks
            valueLabelDisplay="auto"
          />
        );
      case 'select':
        return (
          <FormControl fullWidth>
            <InputLabel>{setting.key}</InputLabel>
            <Select
              value={setting.value}
              onChange={(e) => handleUpdateSetting(setting.key, e.target.value)}
            >
              {/* Add MenuItem options here */}
              <MenuItem value="option1">Option 1</MenuItem>
              <MenuItem value="option2">Option 2</MenuItem>
            </Select>
          </FormControl>
        );
      // Add other case statements for different widget types
      default:
        return (
          <TextField
            value={setting.value}
            onChange={(e) => handleUpdateSetting(setting.key, e.target.value)}
            fullWidth
          />
        );
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
              secondary={renderWidget(setting)}
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
      <FormControl fullWidth margin="normal">
        <InputLabel>Type</InputLabel>
        <Select
          value={newType}
          onChange={(e) => setNewType(e.target.value)}
        >
          <MenuItem value="string">String</MenuItem>
          <MenuItem value="number">Number</MenuItem>
          <MenuItem value="select">Select</MenuItem>
          {/* Add other options here */}
        </Select>
      </FormControl>
      <Button onClick={handleAddSetting} variant="contained" color="primary" style={{ marginTop: '10px' }}>
        Add Setting
      </Button>
      <Button onClick={handleSaveSettings} variant="contained" color="secondary" style={{ marginTop: '10px', marginLeft: '10px' }}>
        Save Settings
      </Button>
    </div>
  );
}

export default ChatbotSettings;