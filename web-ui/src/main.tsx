import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import { ThemeProvider } from '@mui/material/styles';
import theme from './services/theme';
import CssBaseline from '@mui/material/CssBaseline';
import { AuthProvider } from './context/AuthContext';
import './index.css';

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
    <React.StrictMode>
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <AuthProvider>
                <App />
            </AuthProvider>
        </ThemeProvider>
    </React.StrictMode>
);
