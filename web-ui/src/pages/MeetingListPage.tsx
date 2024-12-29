import React, { useEffect, useState } from 'react';
import api from '../services/api';

interface Meeting {
    id: string;
    title: string;
    description: string;
    start_date: string;
    end_date: string;
}

const MeetingListPage: React.FC = () => {
    const [meetings, setMeetings] = useState<Meeting[]>([]);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchMeetings = async () => {
            try {
                const token = localStorage.getItem('authToken');
                if (!token) {
                    throw new Error('No authentication token found');
                }

                const response = await api.get('/meetings', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });
                setMeetings(response.data);
                setError(null);
            } catch (err: any) {
                setError(err.message || 'Failed to fetch meetings');
            }
        };

        fetchMeetings();
    }, []);

    return (
        <div>
            <h1>Meetings</h1>
            {error && <p style={{ color: 'red' }}>{error}</p>}
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
        </div>
    );
};

export default MeetingListPage;
