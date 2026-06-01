import axiosInstance from './axiosInstance';
import { DocumentStatus, DocumentTargetType } from './documentApi';

export interface AuditDocumentItem {
  document_id?: number | null;
  requirement_id: number;
  document_name: string;
  target_type: DocumentTargetType;
  target_id: number;
  target_name: string;
  created_date?: string | null;
  expiration_date?: string | null;
  retention_until?: string | null;
  status: DocumentStatus;
  days_until_expire?: number | null;
  days_until_retention_end?: number | null;
}

export interface AuditOverview {
  missing: AuditDocumentItem[];
  expiring_soon: AuditDocumentItem[];
  retention_ending_soon: AuditDocumentItem[];
}

export interface AuditRecentClient {
  client_id: number;
  client_name: string;
  client_status?: string | null;
  organization_id: number;
}

export interface AuditRecentAssistant {
  assistant_id: number;
  assistant_name: string;
  work_start_date?: string | null;
  organization_id: number;
}

export interface AuditRecentServiceLog {
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

export interface AuditRecentResponse {
  window_years: number;
  cutoff_date: string;
  retention_years: number;
  clients: AuditRecentClient[];
  assistants: AuditRecentAssistant[];
  documents: AuditDocumentItem[];
  service_logs: AuditRecentServiceLog[];
}

export const getAuditOverview = async (): Promise<AuditOverview> => {
  const response = await axiosInstance.get('/api/audit/overview');
  return response.data;
};

export const getAuditRecent = async (): Promise<AuditRecentResponse> => {
  const response = await axiosInstance.get('/api/audit/recent');
  return response.data;
};
