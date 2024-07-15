import React from 'react';
import { Card, CardContent, CardMedia, Typography, IconButton, Box } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import { styled } from '@mui/system';

const StyledCard = styled(Card)(({ theme }) => ({
  display: 'flex',
  flexDirection: 'column',
  height: '200px',
  cursor: 'pointer',
  transition: 'transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out',
  '&:hover': {
    transform: 'translateY(-5px)',
    boxShadow: theme.shadows[8],
  },
}));

const ChatbotThumbnail = ({ chatbot, onSelect, onDelete }) => {
  const getInitials = (name) => {
    return name
      .split(' ')
      .map(word => word[0])
      .join('')
      .toUpperCase()
      .slice(0, 2);
  };

  return (
    <StyledCard onClick={() => onSelect(chatbot)}>
      <CardMedia
        component="div"
        sx={{
          height: 140,
          bgcolor: 'primary.main',
          color: 'primary.contrastText',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: '3rem',
          fontWeight: 'bold',
        }}
      >
        {getInitials(chatbot.name)}
      </CardMedia>
      <CardContent sx={{ flexGrow: 1, display: 'flex', justifyContent: 'space-between', alignItems: 'center', p: 1 }}>
        <Box>
          <Typography variant="subtitle1" noWrap sx={{ fontWeight: 'medium' }}>
            {chatbot.name}
          </Typography>
          <Typography variant="body2" color="text.secondary" noWrap>
            {chatbot.chatbot_type}
          </Typography>
        </Box>
        <IconButton 
          size="small" 
          onClick={(e) => { 
            e.stopPropagation(); 
            onDelete(chatbot.id); 
          }}
          sx={{ 
            color: 'error.main',
            '&:hover': {
              bgcolor: 'error.light',
            },
          }}
        >
          <DeleteIcon />
        </IconButton>
      </CardContent>
    </StyledCard>
  );
};

export default ChatbotThumbnail;