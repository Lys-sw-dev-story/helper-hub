import axiosInstance from './axiosInstance';

export const DocumentTargetType = {
  ORGANIZATION: 'organization',
  CLIENT: 'client',
  ASSISTANT: 'assistant'
} as const;

export type DocumentTargetType = typeof DocumentTargetType[keyof typeof DocumentTargetType];

export const DocumentStatus = {
  NOT_SUBMITTED: '미제출',
  SUBMITTED: '제출완료',
  EXPIRING_SOON: '만료예정'
} as const;

export type DocumentStatus = typeof DocumentStatus[keyof typeof DocumentStatus];

export interface DocumentRequirementCreate {
  target_type: DocumentTargetType;
  document_name: string;
  valid_period_years?: number | null;
}

export interface DocumentRequirementUpdate {
  document_name?: string | null;
  valid_period_years?: number | null;
}

export interface DocumentRequirementResponse {
  requirement_id: number;
  target_type: DocumentTargetType;
  document_name: string;
  valid_period_years?: number | null;
}

export interface DocumentResponse {
  document_id: number;
  requirement_id: number;
  target_id: number;
  file_path?: string | null;
  file_name?: string | null;
  created_date?: string | null;
  expiration_date?: string | null;
  is_submitted: boolean;
  needs_revision: boolean;
  document_memo?: string | null;
  status: DocumentStatus;
}

export interface DocumentUpdate {
  created_date?: string | null;
  document_memo?: string | null;
  expiration_date?: string | null;
  is_submitted?: boolean | null;
  needs_revision?: boolean | null;
}

export interface DocumentChecklistItem {
  requirement_id: number;
  document_name: string;
  valid_period_years?: number | null;
  document_id?: number | null;
  expiration_date?: string | null;
  file_path?: string | null;
  file_name?: string | null;
  status: DocumentStatus;
}

export const listRequirements = async (target_type?: DocumentTargetType): Promise<DocumentRequirementResponse[]> => {
  const response = await axiosInstance.get('/api/documents/requirements', {
    params: { target_type }
  });
  return response.data;
};

export const createRequirement = async (data: DocumentRequirementCreate): Promise<DocumentRequirementResponse> => {
  const response = await axiosInstance.post('/api/documents/requirements', data);
  return response.data;
};

export const updateRequirement = async (id: number, data: DocumentRequirementUpdate): Promise<DocumentRequirementResponse> => {
  const response = await axiosInstance.patch(`/api/documents/requirements/${id}`, data);
  return response.data;
};

export const deleteRequirement = async (id: number): Promise<void> => {
  await axiosInstance.delete(`/api/documents/requirements/${id}`);
};

export const listDocuments = async (target_type?: DocumentTargetType, target_id?: number): Promise<DocumentResponse[]> => {
  const response = await axiosInstance.get('/api/documents', {
    params: { target_type, target_id }
  });
  return response.data;
};

export const getChecklist = async (target_type: DocumentTargetType, target_id: number): Promise<DocumentChecklistItem[]> => {
  const response = await axiosInstance.get('/api/documents/checklist', {
    params: { target_type, target_id }
  });
  return response.data;
};

export const createDocument = async (requirement_id: number, target_id: number, expiration_date?: string, document_memo?: string, file?: File): Promise<DocumentResponse> => {
  const formData = new FormData();
  formData.append('requirement_id', requirement_id.toString());
  formData.append('target_id', target_id.toString());
  if (expiration_date) formData.append('expiration_date', expiration_date);
  if (document_memo) formData.append('document_memo', document_memo);
  if (file) formData.append('file', file);

  const response = await axiosInstance.post('/api/documents', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  return response.data;
};

export const updateDocument = async (id: number, data: DocumentUpdate): Promise<DocumentResponse> => {
  const response = await axiosInstance.patch(`/api/documents/${id}`, data);
  return response.data;
};

export const replaceDocumentFile = async (id: number, file: File): Promise<DocumentResponse> => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await axiosInstance.put(`/api/documents/${id}/file`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  return response.data;
};

export interface SaveDocumentParams {
  requirement_id: number;
  target_id: number;
  document_id?: number | null;
  expiration_date?: string | null;
  document_memo?: string | null;
  file?: File | null;
}

// 체크리스트 행 [변경사항 저장] — 파일+만료일+메모를 한 번에 upsert
export const saveDocument = async (params: SaveDocumentParams): Promise<DocumentResponse> => {
  const formData = new FormData();
  formData.append('requirement_id', params.requirement_id.toString());
  formData.append('target_id', params.target_id.toString());
  if (params.document_id != null) formData.append('document_id', params.document_id.toString());
  if (params.expiration_date) formData.append('expiration_date', params.expiration_date);
  if (params.document_memo) formData.append('document_memo', params.document_memo);
  if (params.file) formData.append('file', params.file);

  const response = await axiosInstance.post('/api/documents/save', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  return response.data;
};

// 첨부 파일 다운로드 (JWT 필요 → axios 로 blob 받아 브라우저 저장 트리거)
export const downloadDocument = async (documentId: number, fileName?: string | null): Promise<void> => {
  const response = await axiosInstance.get(`/api/documents/${documentId}/file`, {
    responseType: 'blob'
  });
  const url = window.URL.createObjectURL(response.data);
  const anchor = window.document.createElement('a');
  anchor.href = url;
  anchor.download = fileName || `document_${documentId}`;
  window.document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  window.URL.revokeObjectURL(url);
};