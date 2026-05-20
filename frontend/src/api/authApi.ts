import axiosInstance from './axiosInstance';

interface LoginRequest {
  email: string;
  password: string;
}

interface LoginResponse {
  access_token: string;
  token_type: string;
}

export const login = async (data: LoginRequest): Promise<LoginResponse> => {
  const response = await axiosInstance.post('/api/auth/login', data);
  return response.data;
};