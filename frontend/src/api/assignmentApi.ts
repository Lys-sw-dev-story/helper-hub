import axiosInstance from './axiosInstance';

// 🚀 백엔드(FastAPI)의 Summary 스키마 구조와 1:1 매칭되는 내부 타입 정의
export interface ClientSummary {
  client_id: number;
  client_name: string;
}

export interface AssistantSummary {
  assistant_id: number;
  assistant_name: string;
  work_days?: string | null;
}

export interface StaffSummary {
  staff_id: number;
  staff_name: string;
}

export interface Assignment {
  assignment_id: number;
  staff_id: number;
  client_id: number;
  assistant_id: number;
  start_date: string;
  end_date: string | null;
  assignment_status: string; // "active" | "ended"

  // 🚀 백엔드 정석 스키마에 맞춰 중첩 객체(Nested Object) 구조 타입 추가!
  client?: ClientSummary | null;
  assistant?: AssistantSummary | null;
  staff?: StaffSummary | null;
}

// 1. 전체 매칭 목록 조회
export const getAssignments = async (): Promise<Assignment[]> => {
  const response = await axiosInstance.get<Assignment[]>('/api/assignments');
  return response.data;
};

// 2. 특정 매칭 상세 조회 (상세 페이지용)
export const getAssignmentById = async (id: number): Promise<Assignment> => {
  const response = await axiosInstance.get<Assignment>(`/api/assignments/${id}`);
  return response.data;
};

// 3. 신규 매칭 등록
export const createAssignment = async (data: Omit<Assignment, 'assignment_id' | 'assignment_status' | 'client' | 'assistant' | 'staff'>): Promise<void> => {
  await axiosInstance.post('/api/assignments', data);
};

// 4. 매칭 종료 처리 (end_date 업데이트 및 상태 변경)
export const endAssignment = async (id: number, endDate: string): Promise<void> => {
  await axiosInstance.patch(`/api/assignments/${id}/end`, { end_date: endDate });
};