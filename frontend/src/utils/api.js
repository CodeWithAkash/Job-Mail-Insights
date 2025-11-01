import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  }
});

// Add response interceptor for better error handling
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      // Redirect to login if unauthorized
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

export const initiateLogin = async () => {
  const response = await api.get('/auth/login');
  return response.data;
};

export const checkAuthStatus = async () => {
  const response = await api.get('/auth/status');
  return response.data;
};

export const logout = async () => {
  const response = await api.post('/auth/logout');
  return response.data;
};

export const fetchEmails = async (forceRefresh = false) => {
  const response = await api.get(`/emails?refresh=${forceRefresh}`);
  return response.data;
};

export const fetchStats = async () => {
  const response = await api.get('/stats');
  return response.data;
};

export const markEmailAsRead = async (emailId) => {
  const response = await api.post(`/emails/${emailId}/read`);
  return response.data;
};

export default api;