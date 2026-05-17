import axiosInstance from './axiosInstance';

export interface AssistantData {
  assistant_name: string;
  assistant_phone?: string;
  work_days?: string;
  work_start_date?: string;
  assistant_license?: string;
  assistant_memo?: string;
  organization_id: number;
}

export const registerAssistant = async (data: AssistantData) => {
  const response = await axiosInstance.post('/assistants', data);
  return response.data;
};

export const getAssistants = async () => {
  const response = await axiosInstance.get('/assistants');
  return response.data;
};