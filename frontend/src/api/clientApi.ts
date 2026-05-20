import axiosInstance from './axiosInstance';

export interface ClientData {
  client_name: string;
  client_birth_date?: string;
  client_phone?: string;
  client_address?: string;
  client_status?: string;
  client_memo?: string;
}

export interface ClientDetail extends ClientData {
  client_id: number;
}

// 1. 이용자 목록 조회
export const getClients = async (): Promise<ClientDetail[]> => {
  const response = await axiosInstance.get('/clients');
  return response.data;
};

// 2. 이용자 상세 조회
export const getClient = async (id: number): Promise<ClientDetail> => {
  const response = await axiosInstance.get(`/clients/${id}`);
  return response.data;
};

// 3. 신규 이용자 등록
export const registerClient = async (data: ClientData) => {
  const response = await axiosInstance.post('/clients', data);
  return response.data;
};

// 4. 이용자 정보 수정 (PATCH)
export const updateClient = async (id: number, data: Partial<ClientData>) => {
  const response = await axiosInstance.patch(`/clients/${id}`, data);
  return response.data;
};

// 5. 이용자 삭제
export const deleteClient = async (id: number) => {
  await axiosInstance.delete(`/clients/${id}`);
};