import axiosInstance from './axiosInstance';

export interface ServiceLogCreate {
  assignment_id: number;
  service_date: string;
  service_hours: number;
  service_count?: number | null;
  service_content?: string | null;
}

export interface ServiceLogUpdate {
  service_date?: string | null;
  service_hours?: number | null;
  service_count?: number | null;
  service_content?: string | null;
}

export interface ServiceLogResponse {
  service_log_id: number;
  assignment_id: number;
  service_date: string;
  service_hours: number;
  service_count?: number | null;
  service_content?: string | null;
  client_id: number;
  client_name: string;
  assistant_id: number;
  assistant_name: string;
}

export const createServiceLog = async (data: ServiceLogCreate): Promise<ServiceLogResponse> => {
  const response = await axiosInstance.post('/api/service-logs', data);
  return response.data;
};

export const listServiceLogs = async (params?: {
  assignment_id?: number;
  client_id?: number;
  assistant_id?: number;
  date_from?: string;
  date_to?: string;
}): Promise<ServiceLogResponse[]> => {
  const response = await axiosInstance.get('/api/service-logs', { params });
  return response.data;
};

export const getServiceLog = async (id: number): Promise<ServiceLogResponse> => {
  const response = await axiosInstance.get(`/api/service-logs/${id}`);
  return response.data;
};

export const updateServiceLog = async (id: number, data: ServiceLogUpdate): Promise<ServiceLogResponse> => {
  const response = await axiosInstance.patch(`/api/service-logs/${id}`, data);
  return response.data;
};

export const deleteServiceLog = async (id: number): Promise<void> => {
  await axiosInstance.delete(`/api/service-logs/${id}`);
};
