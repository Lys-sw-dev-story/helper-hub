import axiosInstance from './axiosInstance';

export interface ClientData {
  client_name: string;
  client_birth_date?: string;
  client_phone?: string;
  client_address?: string;
  client_status?: string;
  client_memo?: string;
  organization_id: number;
}

export interface ClientDetail extends ClientData {
  client_id: number;
}

const normalizeClientList = (data: unknown): ClientDetail[] => {
  if (Array.isArray(data)) {
    return data as ClientDetail[];
  }

  if (
    typeof data === 'object' &&
    data !== null &&
    'clients' in data &&
    Array.isArray((data as { clients: unknown }).clients)
  ) {
    return (data as { clients: ClientDetail[] }).clients;
  }

  if (
    typeof data === 'object' &&
    data !== null &&
    'items' in data &&
    Array.isArray((data as { items: unknown }).items)
  ) {
    return (data as { items: ClientDetail[] }).items;
  }

  return [];
};

// 1. 이용자 목록 조회
// 백엔드가 GET /api/clients 를 허용하고,
// GET /api/clients/ 는 405를 반환하므로 끝의 / 를 붙이지 않는다.
export const getClients = async (): Promise<ClientDetail[]> => {
  const response = await axiosInstance.get('/api/clients');
  return normalizeClientList(response.data);
};

// 2. 이용자 상세 조회
export const getClient = async (id: number): Promise<ClientDetail> => {
  const response = await axiosInstance.get(`/api/clients/${id}`);
  return response.data;
};

// 3. 신규 이용자 등록
// Swagger에서 POST /api/clients/ 로 성공했으므로 등록은 끝의 / 를 유지한다.
export const registerClient = async (data: ClientData): Promise<ClientDetail> => {
  const response = await axiosInstance.post('/api/clients/', data);
  return response.data;
};

// 4. 이용자 정보 수정
export const updateClient = async (
  id: number,
  data: Partial<ClientData>
): Promise<ClientDetail> => {
  const response = await axiosInstance.patch(`/api/clients/${id}`, data);
  return response.data;
};

// 5. 이용자 삭제
export const deleteClient = async (id: number): Promise<void> => {
  await axiosInstance.delete(`/api/clients/${id}`);
};