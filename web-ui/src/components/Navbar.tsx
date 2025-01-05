import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import '../styles/navbar.css';

const NavBar: React.FC = () => {
    const { isLoggedIn } = useAuth();
    console.log('isLoggedIn:', isLoggedIn);

    if (!isLoggedIn) {
        return null;
    }

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
            </ul>
        </nav>
    );
};

export default NavBar;
