import React from 'react';
import { Grid, Typography, TextField, InputAdornment, Box, Fade } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import ChatbotThumbnail from './ChatbotThumbnail';

function ChatbotList({ chatbots, onSelectChatbot, onDeleteChatbot, searchTerm, onSearchChange }) {
  return (
    <Box>
      <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold', color: 'primary.main' }}>
        Your Chatbots
      </Typography>
      <TextField
        fullWidth
        variant="outlined"
        placeholder="Search chatbots..."
        value={searchTerm}
        onChange={onSearchChange}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <SearchIcon color="action" />
            </InputAdornment>
          ),
        }}
        sx={{ mb: 2 }}
      />
      <Grid container spacing={2}>
        {chatbots.map((chatbot, index) => (
          <Fade in={true} timeout={500 + index * 100} key={chatbot.id}>
            <Grid item xs={12} sm={6}>
              <ChatbotThumbnail
                chatbot={chatbot}
                onSelect={onSelectChatbot}
                onDelete={onDeleteChatbot}
              />
            </Grid>
          </Fade>
        ))}
      </Grid>
    </Box>
  );
}

export default ChatbotList;