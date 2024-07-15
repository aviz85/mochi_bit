import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { getChatbots, createChatbot, getChatbotTypes, deleteChatbot } from '../services/api';
import ChatbotList from './ChatbotList';
import ChatWindow from './ChatWindow';
import ChatbotSettings from './ChatbotSettings';
import ChatLogs from './ChatLogs';
import { 
  CssBaseline, Container, Grid, Typography, Button, Tabs, Tab, AppBar, Toolbar, 
  TextField, Dialog, DialogTitle, DialogContent, DialogActions, 
  Select, MenuItem, IconButton, ThemeProvider, createTheme, Box, Fade
} from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import LogoutIcon from '@mui/icons-material/Logout';

// Create a custom theme
const theme = createTheme({
  palette: {
    primary: {
      main: '#6200EA',
    },
    secondary: {
      main: '#03DAC6',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h4: {
      fontWeight: 700,
    },
    h6: {
      fontWeight: 600,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
        },
      },
    },
  },
});


function Dashboard() {
  const [chatbots, setChatbots] = useState([]);
  const [filteredChatbots, setFilteredChatbots] = useState([]);
  const [chatbotTypes, setChatbotTypes] = useState([]);
  const [selectedChatbot, setSelectedChatbot] = useState(null);
  const [activeTab, setActiveTab] = useState(0);
  const [modalOpen, setModalOpen] = useState(false);
  const [newChatbotName, setNewChatbotName] = useState('');
  const [newChatbotType, setNewChatbotType] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const { logout } = useAuth();

  useEffect(() => {
    fetchChatbots();
    fetchChatbotTypes();
  }, []);

  useEffect(() => {
    if (chatbots) {
      setFilteredChatbots(
        chatbots.filter(chatbot => 
          chatbot.name.toLowerCase().includes(searchTerm.toLowerCase())
        )
      );
    }
  }, [chatbots, searchTerm]);

  const fetchChatbots = async () => {
    setIsLoading(true);
    try {
      const response = await getChatbots();
      setChatbots(response.data);
    } catch (error) {
      console.error('Failed to fetch chatbots:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const fetchChatbotTypes = async () => {
    try {
      const response = await getChatbotTypes();
      setChatbotTypes(response.data);
    } catch (error) {
      console.error('Failed to fetch chatbot types:', error);
    }
  };

  const handleCreateChatbot = async () => {
    try {
      const response = await createChatbot(newChatbotName, newChatbotType);
      setChatbots([...chatbots, response.data]);
      setModalOpen(false);
      setNewChatbotName('');
      setNewChatbotType('');
    } catch (error) {
      console.error('Failed to create chatbot:', error);
    }
  };

  const handleDeleteChatbot = async (id) => {
    try {
      await deleteChatbot(id);
      setChatbots(chatbots.filter(chatbot => chatbot.id !== id));
      if (selectedChatbot && selectedChatbot.id === id) {
        setSelectedChatbot(null);
        setActiveTab(0);
      }
    } catch (error) {
      console.error('Failed to delete chatbot:', error);
    }
  };

  const handleSelectChatbot = (chatbot) => {
    setSelectedChatbot(chatbot);
    setActiveTab(0); // Always switch to chat window when a chatbot is selected
  };

  const handleLogout = () => {
    logout();
  };

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
        <AppBar position="static" elevation={0}>
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontWeight: 'bold' }}>
              Mochi Bot
            </Typography>
            <IconButton color="inherit" onClick={handleLogout} edge="end">
              <LogoutIcon />
            </IconButton>
          </Toolbar>
        </AppBar>
        <Container maxWidth="lg" sx={{ mt: 4, mb: 4, flexGrow: 1 }}>
          <Fade in={true} timeout={1000}>
            <Grid container spacing={3}>
              <Grid item xs={12} md={4}>
                <Button 
                  variant="contained" 
                  startIcon={<AddIcon />} 
                  onClick={() => setModalOpen(true)}
                  sx={{ mb: 2, width: '100%' }}
                >
                  New Chatbot
                </Button>
                <ChatbotList
                  chatbots={filteredChatbots}
                  onSelectChatbot={handleSelectChatbot}
                  onDeleteChatbot={handleDeleteChatbot}
                  searchTerm={searchTerm}
                  onSearchChange={(e) => setSearchTerm(e.target.value)}
                />
              </Grid>
              <Grid item xs={12} md={8}>
                {selectedChatbot ? (
                  <Fade in={true} timeout={500}>
                    <Box>
                      <Tabs 
                        value={activeTab} 
                        onChange={handleTabChange}
                        variant="fullWidth"
                        sx={{ mb: 2, bgcolor: 'background.paper', borderRadius: 1 }}
                      >
                        <Tab label="Chat" />
                        <Tab label="Settings" />
                        <Tab label="Chat Logs" />
                      </Tabs>
                      <Box sx={{ p: 2, bgcolor: 'background.paper', borderRadius: 2 }}>
                        {activeTab === 0 && <ChatWindow chatbot={selectedChatbot} />}
                        {activeTab === 1 && <ChatbotSettings chatbotId={selectedChatbot.id} />}
                        {activeTab === 2 && <ChatLogs chatbot={selectedChatbot} />}
                      </Box>
                    </Box>
                  </Fade>
                ) : (
                  <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
                    <Typography variant="h6" color="text.secondary">Select a chatbot to start</Typography>
                  </Box>
                )}
              </Grid>
            </Grid>
          </Fade>
        </Container>
      </Box>

      <Dialog open={modalOpen} onClose={() => setModalOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Create New Chatbot</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Chatbot Name"
            fullWidth
            variant="outlined"
            value={newChatbotName}
            onChange={(e) => setNewChatbotName(e.target.value)}
          />
          <Select
            fullWidth
            value={newChatbotType}
            onChange={(e) => setNewChatbotType(e.target.value)}
            displayEmpty
            variant="outlined"
            sx={{ mt: 2 }}
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
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setModalOpen(false)}>Cancel</Button>
          <Button onClick={handleCreateChatbot} variant="contained" color="primary">
            Create
          </Button>
        </DialogActions>
      </Dialog>
    </ThemeProvider>
  );
}

export default Dashboard;