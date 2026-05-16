import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL, // .env에서 가져온 주소
  headers: {
    'Content-Type': 'application/json',
  },
});

export default axiosInstance;