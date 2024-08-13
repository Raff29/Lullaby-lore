import React from 'react';
import { AppBar, Toolbar, Typography, Button } from '@mui/material';

const Header = () => {
  return (
    <AppBar position="static" sx={{ backgroundColor: 'blue' }}>
      <Toolbar sx={{ justifyContent: 'space-between' }}>
        <Typography variant="h6" sx={{ color: 'white' }}>
          Lullaby Lore
        </Typography>
        <div>
          <Button color="inherit">Home</Button>
          <Button color="inherit">About Us</Button>
          <Button color="inherit">Contact</Button>
        </div>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
