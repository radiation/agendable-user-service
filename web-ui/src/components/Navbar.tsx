import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import '../styles/navbar.css';

const NavBar: React.FC = () => {
    const { isLoggedIn, logout } = useAuth();
    console.log('NavBar isLoggedIn:', isLoggedIn);

    if (!isLoggedIn) {
        return null;
        console.log('NavBar: User not logged in, not rendering');
    }


    const handleLogout = () => {
        if (window.confirm('Are you sure you want to log out?')) {
            logout();
            window.location.href = '/';
        }
    };

    return (
        <nav className="navbar">
            <ul className="navbar-list">
                <li>
                    <Link to="/meetings">My Meetings</Link>
                </li>
                <li>
                    <Link to="/create-meeting">Create Meeting</Link>
                </li>
                <li>
                    <Link to="/tasks">My Tasks</Link>
                </li>
                <li>
                    <button onClick={handleLogout} className="logout-button">
                        Logout
                    </button>
                </li>
            </ul>
        </nav>
    );
};

export default NavBar;
