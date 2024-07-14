import React, { useState } from 'react';
import { List, ListItem, ListItemText, Button, TextField, Select, MenuItem, Typography, IconButton, Dialog, DialogActions, DialogContent, DialogTitle } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';

function ChatbotList({ chatbots, chatbotTypes, onCreateChatbot, onSelectChatbot, onDeleteChatbot }) {
  const [newChatbotName, setNewChatbotName] = useState('');
  const [newChatbotType, setNewChatbotType] = useState('');
  const [confirmDialogOpen, setConfirmDialogOpen] = useState(false);
  const [chatbotToDelete, setChatbotToDelete] = useState(null);

  const handleCreateChatbot = () => {
    if (newChatbotName && newChatbotType) {
      onCreateChatbot(newChatbotName, newChatbotType);
      setNewChatbotName('');
      setNewChatbotType('');
    }
  };

  const handleDeleteChatbot = (chatbot) => {
    setChatbotToDelete(chatbot);
    setConfirmDialogOpen(true);
  };

  const handleConfirmDelete = () => {
    onDeleteChatbot(chatbotToDelete.id);
    setConfirmDialogOpen(false);
    setChatbotToDelete(null);
  };

  const handleCancelDelete = () => {
    setConfirmDialogOpen(false);
    setChatbotToDelete(null);
  };

  return (
    <div>
      <Typography variant="h6" gutterBottom>
        Your Chatbots
      </Typography>
      <List>
        {chatbots.map((chatbot) => (
          <ListItem button key={chatbot.id} onClick={() => onSelectChatbot(chatbot)}>
            <ListItemText primary={chatbot.name} secondary={chatbot.chatbot_type} />
            <IconButton edge="end" aria-label="delete" onClick={(e) => { e.stopPropagation(); handleDeleteChatbot(chatbot); }}>
              <DeleteIcon />
            </IconButton>
          </ListItem>
        ))}
      </List>
      <Typography variant="h6" gutterBottom>
        Create New Chatbot
      </Typography>
      <TextField
        label="Chatbot Name"
        value={newChatbotName}
        onChange={(e) => setNewChatbotName(e.target.value)}
        fullWidth
        margin="normal"
      />
      <Select
        value={newChatbotType}
        onChange={(e) => setNewChatbotType(e.target.value)}
        fullWidth
        displayEmpty
      >
        <MenuItem value="" disabled>
          Select Chatbot Type
        </MenuItem>
        {chatbotTypes.map((type) => (
          <MenuItem key={type.type} value={type.type}>
            {type.name}
          </MenuItem>
        ))}
      </Select>
      <Button onClick={handleCreateChatbot} variant="contained" color="primary" fullWidth>
        Create Chatbot
      </Button>

      <Dialog open={confirmDialogOpen} onClose={handleCancelDelete}>
        <DialogTitle>Confirm Deletion</DialogTitle>
        <DialogContent>
          <Typography>Are you sure you want to delete the chatbot "{chatbotToDelete?.name}"?</Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCancelDelete} color="primary">
            Cancel
          </Button>
          <Button onClick={handleConfirmDelete} color="secondary">
            Delete
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}

export default ChatbotList;