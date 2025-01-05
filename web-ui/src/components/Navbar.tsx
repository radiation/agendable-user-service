import React from 'react';
import { Link } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { useAuth } from '../context/AuthContext';

const NavBar: React.FC = () => {
    const { isLoggedIn, logout } = useAuth();

    if (!isLoggedIn) {
        return null;
    }

    return (
        <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
            <Toolbar>
                <Typography variant="h6" sx={{ flexGrow: 1 }}>
                    Meeting Manager
                </Typography>
                <Box>
                    <Button color="inherit" component={Link} to="/meetings">
                        My Meetings
                    </Button>
                    <Button color="inherit" component={Link} to="/create-meeting">
                        Create Meeting
                    </Button>
                    <Button color="inherit" component={Link} to="/tasks">
                        My Tasks
                    </Button>
                    <Button color="inherit" onClick={logout}>
                        Logout
                    </Button>
                </Box>
            </Toolbar>
        </AppBar>
    );
};

export default NavBar;
