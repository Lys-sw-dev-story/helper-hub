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
  // 기관명을 토큰과 함께 브라우저에 보관
  if (response.data.organization_name) {
    localStorage.setItem('organization_name', response.data.organization_name);
  }
  
  return response.data;
};