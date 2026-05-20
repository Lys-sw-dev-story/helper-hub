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

export interface AssistantDetail extends AssistantData {
  assistant_id: number;
}

// 1. 활동지원사 목록 조회
export const getAssistants = async (): Promise<AssistantDetail[]> => {
  const response = await axiosInstance.get('/api/assistants/');
  return response.data;
};

// 2. 활동지원사 상세 조회
export const getAssistant = async (id: number): Promise<AssistantDetail> => {
  const response = await axiosInstance.get(`/api/assistants/${id}`);
  return response.data;
};

// 3. 신규 활동지원사 등록
export const registerAssistant = async (
  data: AssistantData
): Promise<AssistantDetail> => {
  const response = await axiosInstance.post('/api/assistants/', data);
  return response.data;
};

// 4. 활동지원사 정보 수정
export const updateAssistant = async (
  id: number,
  data: Partial<AssistantData>
): Promise<AssistantDetail> => {
  const response = await axiosInstance.patch(`/api/assistants/${id}`, data);
  return response.data;
};

// 5. 활동지원사 삭제
export const deleteAssistant = async (id: number): Promise<void> => {
  await axiosInstance.delete(`/api/assistants/${id}`);
};