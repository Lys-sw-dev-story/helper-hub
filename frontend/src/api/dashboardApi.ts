import axiosInstance from './axiosInstance';
import { DocumentStatus } from './documentApi';

export interface DashboardCounts {
  client_count: number;
  assistant_count: number;
  active_assignment_count: number;
  not_submitted_document_count: number;
  submitted_document_count: number;
}

export interface DocumentStatusBarItem {
  status: DocumentStatus;
  count: number;
}

export interface DashboardSummary {
  counts: DashboardCounts;
  document_status_chart: DocumentStatusBarItem[];
}

export const getDashboardSummary = async (): Promise<DashboardSummary> => {
  const response = await axiosInstance.get('/api/dashboard/summary');
  return response.data;
};
