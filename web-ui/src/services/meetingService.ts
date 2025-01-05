import api from './api';

interface MeetingPayload {
    title: string;
    start_date: string;
    end_date: string;
    description: string;
}

export const createMeeting = async (meeting: MeetingPayload): Promise<any> => {
    const response = await api.post('/meetings/', meeting);
    return response.data; // Return the created meeting
};

export const getMeetingDetails = async (meetingId: number): Promise<any> => {
    const response = await api.get(`/meetings/${meetingId}`);
    return response.data;
};

export const getUserMeetings = async (userId: number): Promise<any[]> => {
    const response = await api.get(`/meetings/by_user/${userId}`);
    return response.data;
};
