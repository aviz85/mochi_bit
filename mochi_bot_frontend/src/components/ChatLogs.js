import React, { useState, useEffect } from 'react';
import { Typography, List, ListItem, ListItemText, Paper, CircularProgress } from '@mui/material';
import { styled } from '@mui/material/styles';
import { getChatLogs } from '../services/api';

const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(2),
  marginBottom: theme.spacing(2),
  maxHeight: '500px',
  overflow: 'auto',
}));

function ChatLogs({ chatbot }) {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchChatLogs();
  }, [chatbot]);

  const fetchChatLogs = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await getChatLogs(chatbot.id);
      setLogs(Array.isArray(response.data) ? response.data : []);
    } catch (error) {
      console.error('Failed to fetch chat logs:', error);
      if (error.response && error.response.status === 404) {
        setError('Chat logs are not available for this chatbot.');
      } else {
        setError('Failed to fetch chat logs. Please try again later.');
      }
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <CircularProgress />;
  }

  if (error) {
    return <Typography color="error">{error}</Typography>;
  }

  return (
    <div>
      <Typography variant="h5" gutterBottom>
        Chat Logs
      </Typography>
      <StyledPaper>
        {logs.length > 0 ? (
          <List>
            {logs.map((log, index) => (
              <ListItem key={index}>
                <ListItemText
                  primary={`${log.role}: ${log.content}`}
                  secondary={new Date(log.timestamp).toLocaleString()}
                />
              </ListItem>
            ))}
          </List>
        ) : (
          <Typography>No chat logs available for this chatbot.</Typography>
        )}
      </StyledPaper>
    </div>
  );
}

export default ChatLogs;