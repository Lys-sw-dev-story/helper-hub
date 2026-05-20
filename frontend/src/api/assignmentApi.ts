import axiosInstance from './axiosInstance';

export interface Assignment {
  assignment_id: number;
  staff_id: number;
  client_id: number;
  assistant_id: number;
  start_date: string;
  end_date: string | null;
  assignment_status: string; // "active" | "ended"

  // 백엔드에서 Relationship으로 Join해서 보내줄 이용자/지원사 이름
  client_name?: string;
  assistant_name?: string;
}

// 1. 전체 매칭 목록 조회
export const getAssignments = async (): Promise<Assignment[]> => {
  const response = await axiosInstance.get<Assignment[]>('/assignments');
  return response.data;
};

// 2. 특정 매칭 상세 조회 (상세 페이지용)
export const getAssignmentById = async (id: number): Promise<Assignment> => {
  const response = await axiosInstance.get<Assignment>(`/assignments/${id}`);
  return response.data;
};

// 3. 신규 매칭 등록
export const createAssignment = async (data: Omit<Assignment, 'assignment_id' | 'assignment_status'>): Promise<void> => {
  await axiosInstance.post('/assignments', data);
};

// 4. 매칭 종료 처리 (end_date 업데이트 및 상태 변경)
export const endAssignment = async (id: number, endDate: string): Promise<void> => {
  await axiosInstance.patch(`/assignments/${id}/end`, { end_date: endDate });
};