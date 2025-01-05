import React, { useState } from 'react';
import { createMeeting } from '../services/meetingService';

const CreateMeetingPage: React.FC = () => {
    const [title, setTitle] = useState('');
    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');
    const [description, setDescription] = useState('');
    const [message, setMessage] = useState<string | null>(null);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const newMeeting = { title, start_date: startDate, end_date: endDate, description };
            await createMeeting(newMeeting); // Call the service to create a meeting
            setMessage('Meeting created successfully!');
            setTitle('');
            setStartDate('');
            setEndDate('');
            setDescription('');
        } catch (err: any) {
            console.error('Error creating meeting:', err);
            setMessage('Failed to create meeting. Please try again.');
        }
    };

    return (
        <div>
            <h1>Create Meeting</h1>
            {message && <p>{message}</p>}
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="title">Title</label>
                    <input
                        id="title"
                        type="text"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label htmlFor="startDate">Start Date</label>
                    <input
                        id="startDate"
                        type="datetime-local"
                        value={startDate}
                        onChange={(e) => setStartDate(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label htmlFor="endDate">End Date</label>
                    <input
                        id="endDate"
                        type="datetime-local"
                        value={endDate}
                        onChange={(e) => setEndDate(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label htmlFor="description">Description</label>
                    <textarea
                        id="description"
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                        required
                    ></textarea>
                </div>
                <button type="submit">Create Meeting</button>
            </form>
        </div>
    );
};

export default CreateMeetingPage;
