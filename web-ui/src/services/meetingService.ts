import api from './api';

interface MeetingPayload {
    title: string;
    start_date: string;
    end_date: string;
    description: string;
}

export const createMeeting = async (meeting: MeetingPayload): Promise<void> => {
    await api.post('/meetings/', meeting);
};

export const getUserMeetings = async (userId: number): Promise<any[]> => {
    const response = await api.get(`/meetings/by_user/${userId}`);
    return response.data;
};
