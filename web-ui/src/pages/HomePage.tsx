import React, { useEffect, useState } from 'react';
import { getCurrentUser } from '../services/authService';
import { getUserMeetings } from '../services/meetingService';

interface Meeting {
    id: number;
    title: string;
    start_date: string;
    end_date: string;
    description: string;
}

const HomePage: React.FC = () => {
    const [meetings, setMeetings] = useState<Meeting[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                // Fetch the current user
                const user = await getCurrentUser();
                console.log('Current user:', user);

                // Fetch the user's meetings
                const userMeetings = await getUserMeetings(user.id);
                console.log('User meetings:', userMeetings);

                setMeetings(userMeetings);
            } catch (err: any) {
                console.error('Error fetching data:', err);
                setError('Failed to load data.');
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    if (loading) {
        return <p>Loading...</p>;
    }

    if (error) {
        return <p style={{ color: 'red' }}>{error}</p>;
    }

    return (
        <div>
            <h1>Upcoming Meetings</h1>
            {meetings.length === 0 ? (
                <p>No upcoming meetings.</p>
            ) : (
                <ul>
                    {meetings.map((meeting) => (
                        <li key={meeting.id}>
                            <h2>{meeting.title}</h2>
                            <p>{meeting.description}</p>
                            <p>
                                Start: {new Date(meeting.start_date).toLocaleString()}
                            </p>
                            <p>
                                End: {new Date(meeting.end_date).toLocaleString()}
                            </p>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default HomePage;
