import axiosInstance from './axiosInstance';

export const login = async (email: string, password: string) => {
  const response = await axiosInstance.post('/auth/login', {
    email: email,
    password: password,
  });
  
  // 로그인 성공 시 받은 토큰을 브라우저에 저장
  if (response.data.access_token) {
    localStorage.setItem('token', response.data.access_token);
  }
  
  return response.data;
};