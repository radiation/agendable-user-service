import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getMeetingDetails } from '../services/meetingService';

const MeetingDetailsPage: React.FC = () => {
    const { meetingId } = useParams<{ meetingId: string }>();
    const [meeting, setMeeting] = useState<any>(null);
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchMeetingDetails = async () => {
            try {
                const data = await getMeetingDetails(Number(meetingId));
                setMeeting(data);
            } catch (err) {
                console.error('Failed to load meeting details:', err);
                setError('Could not load meeting details.');
            } finally {
                setLoading(false);
            }
        };

        fetchMeetingDetails();
    }, [meetingId]);

    if (loading) return <p>Loading...</p>;
    if (error) return <p style={{ color: 'red' }}>{error}</p>;
    if (!meeting) return <p>No meeting found.</p>;

    return (
        <div>
            <h1>{meeting.title}</h1>
            <p><strong>Start Date:</strong> {new Date(meeting.start_date).toLocaleString()}</p>
            <p><strong>End Date:</strong> {new Date(meeting.end_date).toLocaleString()}</p>
            <p><strong>Duration:</strong> {meeting.duration} minutes</p>
            <p><strong>Location:</strong> {meeting.location}</p>
            <p><strong>Notes:</strong> {meeting.notes}</p>
            <p><strong>Number of Reschedules:</strong> {meeting.num_reschedules}</p>
            <p><strong>Reminder Sent:</strong> {meeting.reminder_sent ? 'Yes' : 'No'}</p>
            <p><strong>Completed:</strong> {meeting.completed ? 'Yes' : 'No'}</p>
            <h2>Attendees</h2>
            {meeting.attendees && meeting.attendees.length > 0 ? (
                <ul>
                    {meeting.attendees.map((attendee: any) => (
                        <li key={attendee.id}>{attendee.name}</li>
                    ))}
                </ul>
            ) : (
                <p>No attendees found.</p>
            )}

            <h2>Tasks</h2>
            {meeting.tasks && meeting.tasks.length > 0 ? (
                <ul>
                    {meeting.tasks.map((task: any) => (
                        <li key={task.id}>{task.description}</li>
                    ))}
                </ul>
            ) : (
                <p>No tasks found.</p>
            )}
        </div>
    );
};

export default MeetingDetailsPage;
