import React, { useEffect, useState } from 'react';
import { Meeting } from '../types/meeting';
import { getAllMeetings } from '../services/meetingService';
import MeetingList from '../components/MeetingList';
import { Container, Typography, CircularProgress, Alert } from '@mui/material';

const MeetingsPage: React.FC = () => {
  const [meetings, setMeetings] = useState<Meeting[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchMeetings = async () => {
      try {
        const data = await getAllMeetings();
        setMeetings(data);
      } catch (err) {
        console.error('Failed to load meetings:', err);
        setError('Could not load meetings.');
      } finally {
        setLoading(false);
      }
    };

    fetchMeetings();
  }, []);

  if (loading) {
    return (
      <Container maxWidth="md" sx={{ mt: 4 }}>
        <CircularProgress />
      </Container>
    );
  }

  if (error) {
    return (
      <Container maxWidth="md" sx={{ mt: 4 }}>
        <Alert severity="error">{error}</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>
        All Meetings
      </Typography>
      <MeetingList meetings={meetings} />
    </Container>
  );
};

export default MeetingsPage;
