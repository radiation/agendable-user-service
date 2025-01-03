import api from './api';

export const getUserMeetings = async (userId: number): Promise<any[]> => {
    const response = await api.get(`/meetings/by_user/${userId}`);
    return response.data;
};
