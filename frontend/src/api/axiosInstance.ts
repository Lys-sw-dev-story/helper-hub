import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL, // .env에서 가져온 주소
  headers: {
    'Content-Type': 'application/json',
  },
});

// 나중에 여기에 "로그인 토큰 자동 첨부" 로직을 넣을 거야!
export default axiosInstance;