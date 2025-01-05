import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createMeeting } from '../services/meetingService';
import {
    Container,
    TextField,
    Button,
    Typography,
    Box,
    Alert,
} from '@mui/material';

const CreateMeetingPage: React.FC = () => {
    const navigate = useNavigate();
    const [title, setTitle] = useState('');
    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');
    const [description, setDescription] = useState('');
    const [message, setMessage] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const newMeeting = { title, start_date: startDate, end_date: endDate, description };
            const createdMeeting = await createMeeting(newMeeting);
            setMessage('Meeting created successfully!');
            setError(null);
            setTitle('');
            setStartDate('');
            setEndDate('');
            setDescription('');
            navigate(`/meetings/${createdMeeting.id}`);
        } catch (err: any) {
            console.error('Error creating meeting:', err);
            setError('Failed to create meeting. Please try again.');
        }
    };

    return (
        <Container maxWidth="sm">
            <Box sx={{ mt: 4, mb: 2 }}>
                <Typography variant="h4" component="h1" gutterBottom>
                    Create Meeting
                </Typography>
                {message && <Alert severity="success">{message}</Alert>}
                {error && <Alert severity="error">{error}</Alert>}
            </Box>
            <form onSubmit={handleSubmit}>
                <TextField
                    label="Title"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    fullWidth
                    margin="normal"
                    required
                />
                <TextField
                    label="Start Date"
                    type="datetime-local"
                    value={startDate}
                    onChange={(e) => setStartDate(e.target.value)}
                    fullWidth
                    margin="normal"
                    InputLabelProps={{ shrink: true }}
                    required
                />
                <TextField
                    label="End Date"
                    type="datetime-local"
                    value={endDate}
                    onChange={(e) => setEndDate(e.target.value)}
                    fullWidth
                    margin="normal"
                    InputLabelProps={{ shrink: true }}
                    required
                />
                <TextField
                    label="Description"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    fullWidth
                    margin="normal"
                    multiline
                    rows={4}
                    required
                />
                <Button type="submit" variant="contained" color="primary" fullWidth>
                    Create Meeting
                </Button>
            </form>
        </Container>
    );
};

export default CreateMeetingPage;
