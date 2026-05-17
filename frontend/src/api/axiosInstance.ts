// frontend/src/api/axiosInstance.ts
import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ✅ Axios로 요청을 보내기 직전에 브라우저 창고에서 토큰을 꺼내 헤더에 가로채서 넣어줌
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`; // 백엔드가 요구하는 Bearer 토큰 규격
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default axiosInstance;