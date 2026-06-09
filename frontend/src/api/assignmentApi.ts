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
  assistant_support_types?: string | null;
}

// 🚀 태그 매칭(배정 후보) 응답 타입 — 백엔드 MatchCandidatesResponse 와 1:1
export interface MatchCandidate {
  assistant_id: number;
  assistant_name: string;
  assistant_phone?: string | null;
  work_days: string[];
  support_types: string[];
  matched_days: string[];
  matched_support: string[];
  is_full_match: boolean;
  already_assigned: boolean;
}

export interface MatchCandidatesResponse {
  client_id: number;
  client_name: string;
  preferred_days: string[];
  support_types: string[];
  candidate_count: number;
  candidates: MatchCandidate[];
}

export interface CreateAssignmentPayload {
  client_id: number;
  assistant_id: number;
  start_date: string;
  end_date?: string | null;
  // staff_id 는 보내지 않으면 로그인한 staff(매칭 담당자)로 백엔드가 자동 설정한다.
  staff_id?: number;
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

// 3. 신규 매칭 등록 (staff_id 는 백엔드가 로그인 staff 로 자동 설정)
export const createAssignment = async (data: CreateAssignmentPayload): Promise<void> => {
  await axiosInstance.post('/api/assignments', data);
};

// 4. 매칭 종료 처리 (end_date 업데이트 및 상태 변경)
export const endAssignment = async (id: number, endDate: string): Promise<void> => {
  await axiosInstance.patch(`/api/assignments/${id}/end`, { end_date: endDate });
};

// 5. 이용자 태그 조건에 맞는 활동지원사 후보 조회 (배정 매칭용)
export const getMatchCandidates = async (
  clientId: number
): Promise<MatchCandidatesResponse> => {
  const response = await axiosInstance.get<MatchCandidatesResponse>(
    '/api/assignments/match-candidates',
    { params: { client_id: clientId } }
  );
  return response.data;
};