/**
 * API Service - Axios wrapper for Yemen LPR API
 */
import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE ?? '';
const API_VERSION = '/api/v1';

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 300000,
});

// Request interceptor to add API key
apiClient.interceptors.request.use(
  (config) => {
    const apiKey = localStorage.getItem('yemen_lpr_api_key');
    if (apiKey) {
      config.headers['X-API-Key'] = apiKey;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    let message = 'حدث خطأ غير متوقع';
    
    if (error.response) {
      // Server responded with error
      const status = error.response.status;
      const data = error.response.data;
      
      if (status === 400) {
        message = data.error || data.detail || 'الملف غير مدعوم أو تالف';
      } else if (status === 401) {
        message = 'مفتاح API غير صحيح أو منتهي الصلاحية';
      } else if (status === 413) {
        message = 'حجم الملف كبير جداً. الحد الأقصى 100MB';
      } else if (status === 429) {
        message = data.message || 'تجاوزت الحد المسموح. انتظر دقيقة وحاول مجدداً.';
      } else if (status === 500) {
        message = 'خطأ في الخادم. يرجى المحاولة لاحقاً';
      } else {
        message = data.error || data.detail || `خطأ في الخادم (${status})`;
      }
    } else if (error.request) {
      // Request made but no response
      if (error.code === 'ECONNABORTED' || error.message?.includes('timeout')) {
        message = 'انتهت مهلة الاتصال. يرجى المحاولة مرة أخرى';
      } else {
        message = 'فشل الاتصال بالخادم. تحقق من الاتصال بالإنترنت';
      }
    } else {
      message = error.message || 'حدث خطأ غير متوقع';
    }
    
    return Promise.reject({ ...error, message });
  }
);

export const api = {
  // Health check
  health: () => apiClient.get(`${API_VERSION}/health/`),

  // Image prediction
  predictImage: (file, overlay = true) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('overlay', overlay);
    return apiClient.post(`${API_VERSION}/predict/image/`, formData);
  },

  // Video prediction
  predictVideo: (file, skipFrames = 2) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('skip_frames', skipFrames);
    return apiClient.post(`${API_VERSION}/predict/video/`, formData);
  },

  // API Key management (JSON body)
  createApiKey: (name) => {
    return apiClient.post(`${API_VERSION}/api-keys/create/`, { name }, {
      headers: { 'Content-Type': 'application/json' },
    });
  },
};

export default api;
