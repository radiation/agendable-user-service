import React, { useEffect, useState } from 'react';
import { Meeting } from '../types/meeting';
import { getCurrentUser } from '../services/authService';
import { getUserMeetings } from '../services/meetingService';
import MeetingList from '../components/MeetingList';
import { Container, Typography, CircularProgress, Alert } from '@mui/material';

const HomePage: React.FC = () => {
  const [meetings, setMeetings] = useState<Meeting[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch the current user
        const user = await getCurrentUser();

        // Fetch the user's meetings
        const userMeetings = await getUserMeetings(user.id);

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
        Upcoming Meetings
      </Typography>
      <MeetingList meetings={meetings} />
    </Container>
  );
};

export default HomePage;
