import React, { useState, useEffect } from 'react';
import { TextField, Slider, Switch, Button, Typography, Grid, CircularProgress } from '@mui/material';
import { getChatbotSettings, updateChatbotSettings } from '../services/api';

const ChatbotSettings = ({ chatbotId }) => {
  const [settings, setSettings] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchSettings = async () => {
      if (chatbotId) {
        try {
          setLoading(true);
          const fetchedSettings = await getChatbotSettings(chatbotId);
          setSettings(fetchedSettings);
        } catch (err) {
          setError('Failed to load settings');
          console.error('Error fetching settings:', err);
        } finally {
          setLoading(false);
        }
      }
    };

    fetchSettings();
  }, [chatbotId]);

  const handleSettingChange = (key, value) => {
    setSettings(prevSettings => ({
      ...prevSettings,
      [key]: { ...prevSettings[key], value }
    }));
  };

  const handleSaveSettings = async () => {
    try {
      setLoading(true);
      const updatedSettings = Object.entries(settings).reduce((acc, [key, setting]) => {
        acc[key] = setting.value;
        return acc;
      }, {});
      const response = await updateChatbotSettings(chatbotId, updatedSettings);
      setSettings(response);
      setError(null);
    } catch (err) {
      setError('Failed to save settings');
      console.error('Error saving settings:', err);
    } finally {
      setLoading(false);
    }
  };

  const renderSettingInput = (key, setting) => {
    switch (setting.type) {
      case 'number':
        return (
          <Slider
            value={setting.value}
            onChange={(_, newValue) => handleSettingChange(key, newValue)}
            min={0}
            max={1}
            step={0.1}
            valueLabelDisplay="auto"
          />
        );
      case 'boolean':
        return (
          <Switch
            checked={setting.value}
            onChange={(e) => handleSettingChange(key, e.target.checked)}
          />
        );
      default:
        return (
          <TextField
            value={setting.value}
            onChange={(e) => handleSettingChange(key, e.target.value)}
            fullWidth
          />
        );
    }
  };

  if (loading) return <CircularProgress />;
  if (error) return <Typography color="error">{error}</Typography>;

  return (
    <Grid container spacing={2}>
      <Grid item xs={12}>
        <Typography variant="h6">Chatbot Settings</Typography>
      </Grid>
      {Object.entries(settings).map(([key, setting]) => (
        <Grid item xs={12} key={key}>
          <Typography>{setting.display_name || key}</Typography>
          <Typography variant="body2">{setting.description}</Typography>
          {renderSettingInput(key, setting)}
        </Grid>
      ))}
      <Grid item xs={12}>
        <Button 
          onClick={handleSaveSettings} 
          variant="contained" 
          color="primary"
          disabled={loading}
        >
          {loading ? <CircularProgress size={24} /> : 'Save Settings'}
        </Button>
      </Grid>
    </Grid>
  );
};

export default ChatbotSettings;