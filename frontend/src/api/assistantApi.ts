import axiosInstance from './axiosInstance';

export interface AssistantData {
  assistant_name: string;
  assistant_phone?: string;
  work_days?: string; // 매칭 태그: 근무 가능 요일 CSV ("월,수,금")
  assistant_support_types?: string; // 매칭 태그: 가능 지원 분야 CSV
  work_start_date?: string;
  assistant_license?: string;
  assistant_memo?: string;
  organization_id: number;
}

export interface AssistantDetail extends AssistantData {
  assistant_id: number;
}

export interface TenureInfo {
  work_start_date: string | null;
  reference_date: string;
  years: number;
  months: number;
  days: number;
  total_days: number;
}

export interface MonthlyWorkHours {
  month: number;
  service_hours: number;
  service_count: number;
}

export interface AssistantWorkHoursSummary {
  assistant_id: number;
  assistant_name: string;
  year: number;
  yearly_hours: number;
  yearly_count: number;
  cumulative_hours: number;
  cumulative_count: number;
  monthly: MonthlyWorkHours[];
}

export interface AssistantPayrollTenureItem {
  assistant_id: number;
  assistant_name: string;
  work_start_date: string | null;
  work_days: string | null;
  tenure: TenureInfo;
  yearly_hours: number;
  cumulative_hours: number;
  active_assignment_count: number;
  assistant_memo: string | null;
}

export interface AssistantPayrollTenureResponse {
  year: number;
  reference_date: string;
  items: AssistantPayrollTenureItem[];
}

// 1. 활동지원사 목록 조회 (끝 주소 깔끔하게 정돈)
export const getAssistants = async (): Promise<AssistantDetail[]> => {
  const response = await axiosInstance.get('/api/assistants');
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
  const response = await axiosInstance.post('/api/assistants', data);
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

// 6. 활동지원사 전체 급여·근속 조회
export const getPayrollTenure = async (year?: number): Promise<AssistantPayrollTenureResponse> => {
  const response = await axiosInstance.get('/api/assistants/payroll-tenure', {
    params: { year }
  });
  return response.data;
};

// 7. 특정 활동지원사 근속 조회
export const getAssistantTenure = async (id: number): Promise<TenureInfo> => {
  const response = await axiosInstance.get(`/api/assistants/${id}/tenure`);
  return response.data;
};

// 8. 특정 활동지원사 근로시간 조회
export const getAssistantWorkHours = async (id: number, year?: number): Promise<AssistantWorkHoursSummary> => {
  const response = await axiosInstance.get(`/api/assistants/${id}/work-hours`, {
    params: { year }
  });
  return response.data;
};