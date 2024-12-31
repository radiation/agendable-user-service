import api from './api';

export const login = async (email: string, password: string): Promise<string> => {
    const response = await api.post('/auth/login', {
        email,
        password,
    });

    return response.data.access_token;
};
