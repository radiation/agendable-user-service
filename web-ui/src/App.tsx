import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import MeetingListPage from './pages/MeetingListPage';

const App: React.FC = () => {
    return (
        <Router>
            <Routes>
                {/* Route for the login page */}
                <Route path="/" element={<LoginPage />} />
                {/* Route for the meetings list */}
                <Route path="/meetings" element={<MeetingListPage />} />
            </Routes>
        </Router>
    );
};

export default App;
