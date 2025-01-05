import React from 'react';
import { Link } from 'react-router-dom';
import {
  List,
  ListItem,
  ListItemText,
  ListItemButton,
  Typography,
} from '@mui/material';

interface Meeting {
  id: number;
  title: string;
  start_date: string;
  end_date: string;
  description: string;
}

interface MeetingListProps {
  meetings: Meeting[];
}

const MeetingList: React.FC<MeetingListProps> = ({ meetings }) => {
  if (meetings.length === 0) {
    return <Typography>No meetings found.</Typography>;
  }

  return (
    <List>
      {meetings.map((meeting) => (
        <ListItem key={meeting.id} disablePadding>
          <ListItemButton component={Link} to={`/meetings/${meeting.id}`}>
            <ListItemText
              primary={meeting.title}
              secondary={`Start: ${new Date(meeting.start_date).toLocaleString()} | End: ${new Date(
                meeting.end_date
              ).toLocaleString()}`}
            />
          </ListItemButton>
        </ListItem>
      ))}
    </List>
  );
};

export default MeetingList;
