import axiosInstance from './axiosInstance';

export interface AssistantData {
  assistant_name: string;
  assistant_phone?: string;
  work_days?: string;
  work_start_date?: string;
  assistant_license?: string;
  assistant_memo?: string;
}

// 목록 및 상세 조회 시 ID가 포함된 데이터 타입
export interface AssistantDetail extends AssistantData {
  assistant_id: number;
}

// 1. 활동지원사 전체 목록 조회 (GET /assistants)
export const getAssistants = async (): Promise<AssistantDetail[]> => {
  const response = await axiosInstance.get('/assistants');
  return response.data;
};

// 2. 활동지원사 상세 조회 (GET /assistants/{id})
export const getAssistant = async (id: number): Promise<AssistantDetail> => {
  const response = await axiosInstance.get(`/assistants/${id}`);
  return response.data;
};

// 3. 신규 활동지원사 등록 (POST /assistants)
export const registerAssistant = async (data: AssistantData) => {
  const response = await axiosInstance.post('/assistants', data);
  return response.data;
};

<<<<<<< HEAD
export const getAssistants = async () => {
  const response = await axiosInstance.get('/assistants');
  return response.data;
=======
// 4. 활동지원사 정보 수정 (PATCH /assistants/{id})
export const updateAssistant = async (id: number, data: Partial<AssistantData>) => {
  const response = await axiosInstance.patch(`/assistants/${id}`, data);
  return response.data;
};

// 5. 활동지원사 삭제 (DELETE /assistants/{id})
export const deleteAssistant = async (id: number) => {
  await axiosInstance.delete(`/assistants/${id}`);
>>>>>>> 2week
};