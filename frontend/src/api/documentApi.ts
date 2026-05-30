import axiosInstance from './axiosInstance';

export type DocumentTargetType = 'client' | 'assistant';

export type DocumentStatus = 
  | 'not_submitted'
  | 'submitted'
  | 'expiring_soon'
  | 'expired'
  | 'needs_revision';

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
  document_id?: number | null;
  created_date?: string | null;
  expiration_date?: string | null;
  is_submitted: boolean;
  needs_revision: boolean;
  document_memo?: string | null;
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

export const upsertDocument = async (requirement_id: number, target_id: number, data: DocumentUpdate): Promise<DocumentResponse> => {
  const response = await axiosInstance.put('/api/documents', {
    requirement_id,
    target_id,
    ...data
  });
  return response.data;
};
