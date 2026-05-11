// src/api/clientApi.ts
import axiosInstance from './axiosInstance';

export interface ClientData {
  client_name: string;
  client_birth_date?: string | null; 
  client_phone?: string | null;     
  client_address?: string | null;
  client_status?: string | null;
  client_memo?: string | null;
  organization_id: number;
}

export const registerClient = async (clientData: ClientData) => {
  const response = await axiosInstance.post('/clients', clientData);
  return response.data;
};

export const getClients = async () => {
  const response = await axiosInstance.get('/clients');
  return response.data;
};