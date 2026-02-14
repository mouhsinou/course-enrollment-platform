import axios from 'axios';

const api = axios.create({
    baseURL: '/', // Proxy handles the base URL
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add a request interceptor to attach the token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Add a response interceptor to handle errors
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && error.response.status === 401) {
            // Auto logout if 401 (optional, depends on UX)
            // localStorage.removeItem('token');
            // window.location.href = '/login'; 
            // Better to handle in AuthContext
        }
        return Promise.reject(error);
    }
);

export default api;
