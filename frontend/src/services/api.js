import axios from 'axios';

const API = axios.create({
  baseURL: 'http://127.0.0.1:5000/api',
});

API.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth
export const register = (data) => API.post('/auth/register', data);
export const login    = (data) => API.post('/auth/login', data);
export const logout   = ()     => API.post('/auth/logout');

// Content
export const getContent       = (params) => API.get('/content/', { params });
export const searchContent    = (q)      => API.get('/content/search', { params: { q } });
export const getContentById   = (id)     => API.get(`/content/${id}`);

// Interactions
export const logInteraction      = (data) => API.post('/interactions/', data);
export const getUserInteractions = ()     => API.get('/interactions/');

// Recommendations
export const generateRecommendations = () => API.post('/recommendations/generate');
export const getRecommendations      = ()  => API.get('/recommendations/');
export const markClicked             = (id) => API.post(`/recommendations/click/${id}`);
export const saveRecommendation = (id)       => API.post(`/recommendations/save/${id}`);
export const saveContent        = (contentId) => API.post(`/recommendations/save-content/${contentId}`);
export const getSaved           = ()          => API.get('/recommendations/saved');
export default API;