import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 20000 // 20 second timeout
});

// Add response interceptor for better error handling
api.interceptors.response.use(
  response => response,
  error => {
    if (error.code === 'ECONNABORTED') {
      console.log('Request timeout');
    }
    if (error.response?.status === 401) {
      // Don't redirect on 401 during auth check
      console.log('Not authenticated');
    }
    return Promise.reject(error);
  }
);

export const initiateLogin = async () => {
  const response = await api.get('/auth/login');
  return response.data;
};

export const checkAuthStatus = async () => {
  try {
    const response = await api.get('/auth/status');
    return response.data;
  } catch (error) {
    if (error.response?.status === 401) {
      return { authenticated: false };
    }
    throw error;
  }
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