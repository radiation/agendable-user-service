import axios from 'axios';

// Create an Axios instance
const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add a request interceptor to attach the Authorization header
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('authToken');
        console.log('Attaching token to request:', token); // Debug log

        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        console.log('Request headers:', config.headers); // Debug log
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

export default api;
