import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import HomePage from './pages/HomePage';
import MeetingsPage from './pages/MeetingsPage';
import CreateMeetingPage from './pages/CreateMeetingPage';
import TasksPage from './pages/TasksPage';
import NavBar from './components/NavBar';

const App: React.FC = () => (
    <Router>
        <div className="app-layout">
            <NavBar />
            <Routes>
                <Route path="/" element={<LoginPage />} />
                <Route path="/home" element={<HomePage />} />
                <Route path="/meetings" element={<MeetingsPage />} />
                <Route path="/create-meeting" element={<CreateMeetingPage />} />
                <Route path="/tasks" element={<TasksPage />} />
            </Routes>
        </div>
    </Router>
);

export default App;
