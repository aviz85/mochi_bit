import React, { useState, useEffect } from 'react';
import { Typography, List, ListItem, ListItemText, Paper, CircularProgress, Accordion, AccordionSummary, AccordionDetails } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { styled } from '@mui/material/styles';
import { getChatLogs } from '../services/api';

const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(2),
  marginBottom: theme.spacing(2),
  maxHeight: '500px',
  overflow: 'auto',
}));

const StyledAccordion = styled(Accordion)(({ theme }) => ({
  marginBottom: theme.spacing(1),
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
      const data = await getChatLogs(chatbot.id);
      setLogs(Array.isArray(data) ? data.filter(thread => thread.messages.length > 0) : []);
    } catch (error) {
      console.error('Failed to fetch chat logs:', error);
      setError('Failed to fetch chat logs. Please try again later.');
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
          logs.map((thread, index) => (
            <StyledAccordion key={thread.thread_id}>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography>Thread {index + 1} - {new Date(thread.created_at).toLocaleString()} ({thread.messages.length} messages)</Typography>
              </AccordionSummary>
              <AccordionDetails>
                <List>
                  {thread.messages.map((message, msgIndex) => (
                    <ListItem key={msgIndex}>
                      <ListItemText
                        primary={`${message.role}: ${message.content}`}
                        secondary={new Date(message.created_at).toLocaleString()}
                      />
                    </ListItem>
                  ))}
                </List>
              </AccordionDetails>
            </StyledAccordion>
          ))
        ) : (
          <Typography>No chat logs available for this chatbot.</Typography>
        )}
      </StyledPaper>
    </div>
  );
}

export default ChatLogs;