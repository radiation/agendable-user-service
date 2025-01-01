import api from './api';

export const getUserMeetings = async (userId: number): Promise<any[]> => {
    const response = await api.get(`/user_meetings/${userId}`);
    return response.data;
};
