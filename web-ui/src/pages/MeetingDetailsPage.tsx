import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getMeetingDetails } from '../services/meetingService';
import {
  Container,
  Typography,
  CircularProgress,
  Alert,
  List,
  ListItem,
  ListItemText,
  Divider,
} from '@mui/material';

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

  if (loading)
    return (
      <Container maxWidth="md" sx={{ mt: 4 }}>
        <CircularProgress />
      </Container>
    );
  if (error)
    return (
      <Container maxWidth="md" sx={{ mt: 4 }}>
        <Alert severity="error">{error}</Alert>
      </Container>
    );
  if (!meeting)
    return (
      <Container maxWidth="md" sx={{ mt: 4 }}>
        <Typography>No meeting found.</Typography>
      </Container>
    );

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>
        {meeting.title}
      </Typography>
      <Typography variant="body1">
        <strong>Start Date:</strong>{' '}
        {new Date(meeting.start_date).toLocaleString()}
      </Typography>
      <Typography variant="body1">
        <strong>End Date:</strong>{' '}
        {new Date(meeting.end_date).toLocaleString()}
      </Typography>
      <Typography variant="body1">
        <strong>Duration:</strong> {meeting.duration} minutes
      </Typography>
      <Typography variant="body1">
        <strong>Location:</strong> {meeting.location}
      </Typography>
      <Typography variant="body1">
        <strong>Notes:</strong> {meeting.notes}
      </Typography>
      <Typography variant="body1">
        <strong>Number of Reschedules:</strong> {meeting.num_reschedules}
      </Typography>
      <Typography variant="body1">
        <strong>Reminder Sent:</strong> {meeting.reminder_sent ? 'Yes' : 'No'}
      </Typography>
      <Typography variant="body1">
        <strong>Completed:</strong> {meeting.completed ? 'Yes' : 'No'}
      </Typography>

      <Divider sx={{ my: 2 }} />

      <Typography variant="h5" gutterBottom>
        Attendees
      </Typography>
      {meeting.attendees && meeting.attendees.length > 0 ? (
        <List>
          {meeting.attendees.map((attendee: any) => (
            <ListItem key={attendee.id}>
              <ListItemText primary={attendee.name} />
            </ListItem>
          ))}
        </List>
      ) : (
        <Typography>No attendees found.</Typography>
      )}

      <Divider sx={{ my: 2 }} />

      <Typography variant="h5" gutterBottom>
        Tasks
      </Typography>
      {meeting.tasks && meeting.tasks.length > 0 ? (
        <List>
          {meeting.tasks.map((task: any) => (
            <ListItem key={task.id}>
              <ListItemText primary={task.description} />
            </ListItem>
          ))}
        </List>
      ) : (
        <Typography>No tasks found.</Typography>
      )}
    </Container>
  );
};

export default MeetingDetailsPage;
