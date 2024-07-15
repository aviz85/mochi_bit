import React, { useState, useEffect } from 'react';
import { TextField, Slider, Switch, Button, Typography, Grid, CircularProgress, Snackbar, Alert } from '@mui/material';
import { getChatbotSettings, updateChatbotSettings } from '../services/api';

const ChatbotSettings = ({ chatbotId }) => {
  const [settings, setSettings] = useState({});
  const [loading, setLoading] = useState(true);
  const [toast, setToast] = useState({ open: false, message: '', severity: 'success' });

  useEffect(() => {
    fetchSettings();
  }, [chatbotId]);

  const fetchSettings = async () => {
    if (chatbotId) {
      try {
        setLoading(true);
        const fetchedSettings = await getChatbotSettings(chatbotId);
        setSettings(fetchedSettings);
      } catch (err) {
        console.error('Error fetching settings:', err);
        showToast('Failed to load settings', 'error');
      } finally {
        setLoading(false);
      }
    }
  };

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
      await updateChatbotSettings(chatbotId, updatedSettings);
      showToast('Settings saved successfully', 'success');
    } catch (err) {
      console.error('Error saving settings:', err);
      showToast('Failed to save settings', 'error');
    } finally {
      setLoading(false);
    }
  };

  const showToast = (message, severity) => {
    setToast({ open: true, message, severity });
  };

  const handleCloseToast = (event, reason) => {
    if (reason === 'clickaway') return;
    setToast({ ...toast, open: false });
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

  if (loading && Object.keys(settings).length === 0) return <CircularProgress />;

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
      <Snackbar open={toast.open} autoHideDuration={6000} onClose={handleCloseToast}>
        <Alert onClose={handleCloseToast} severity={toast.severity} sx={{ width: '100%' }}>
          {toast.message}
        </Alert>
      </Snackbar>
    </Grid>
  );
};

export default ChatbotSettings;