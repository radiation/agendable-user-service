import api from './api';

export const login = async (email: string, password: string): Promise<string> => {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    console.log("Base URL:", import.meta.env.VITE_API_BASE_URL);
    console.log("FormData being sent:", email, password);

    const response = await api.post('/auth/jwt/login', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });

    return response.data.access_token;
};
