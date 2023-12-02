import React from 'react';
import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import AppBar from '@mui/material/AppBar';
import CssBaseline from '@mui/material/CssBaseline';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Sidebar from './Sidebar'
import { createTheme, ThemeProvider } from '@mui/material/styles';
import GlassCollectionMap from './components/GlassCollectionMap';

// Create a custom theme with the desired primary color
const theme = createTheme({
  palette: {
    primary: {
      main: '#16A74E', // Change this to your desired color
    },
  },
});

const drawerWidth = 360;

const App = () => {

  return (
    <ThemeProvider theme={theme}>
      <Box sx={{ display: 'flex' }}>
        <CssBaseline />
        <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
          <Toolbar>
            <Typography variant="h6" noWrap component="div">
              SG - Glass Collection Predictor
            </Typography>
          </Toolbar>
        </AppBar>
        <Drawer
          variant="permanent"
          sx={{
            width: drawerWidth,
            flexShrink: 0,
            [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' },
          }}
        >
          <Toolbar />
          <Box sx={{ overflow: 'auto' }}>

            <Sidebar />

          </Box>
        </Drawer>
        <Box component="main" sx={{ flexGrow: 1 }}>
          <Toolbar />

            <GlassCollectionMap />

        </Box>
      </Box>
    </ThemeProvider>
  );
};

export default App;