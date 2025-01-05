import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { CssBaseline, Toolbar } from '@mui/material';
import LoginPage from './pages/LoginPage';
import HomePage from './pages/HomePage';
import MeetingListPage from './pages/MeetingListPage';
import CreateMeetingPage from './pages/CreateMeetingPage';
import MeetingDetailsPage from './pages/MeetingDetailsPage';
import TasksPage from './pages/TasksPage';
import NavBar from './components/Navbar';

const App: React.FC = () => (
    <Router>
        <div className="app-layout">
            <NavBar />
            <CssBaseline />
            <Toolbar />
            <Routes>
                <Route path="/" element={<LoginPage />} />
                <Route path="/home" element={<HomePage />} />
                <Route path="/meetings" element={<MeetingListPage />} />
                <Route path="/create-meeting" element={<CreateMeetingPage />} />
                <Route path="/meetings/:meetingId" element={<MeetingDetailsPage />} />
                <Route path="/tasks" element={<TasksPage />} />
            </Routes>
        </div>
    </Router>
);

export default App;
