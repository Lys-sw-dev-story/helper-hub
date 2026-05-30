import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';
import { createServiceLog, getServiceLog, updateServiceLog } from '../../api/serviceLogApi';
import './ServiceLogList.css'; // We'll reuse/extend the existing CSS

const ServiceLogForm: React.FC = () => {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const isEditMode = Boolean(id);

  const [assignmentId, setAssignmentId] = useState<string>('');
  const [serviceDate, setServiceDate] = useState<string>('');
  const [serviceHours, setServiceHours] = useState<string>('');
  const [serviceCount, setServiceCount] = useState<string>('');
  const [serviceContent, setServiceContent] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(isEditMode);

  useEffect(() => {
    if (isEditMode) {
      const fetchLog = async () => {
        try {
          const data = await getServiceLog(Number(id));
          setAssignmentId(String(data.assignment_id));
          setServiceDate(data.service_date);
          setServiceHours(String(data.service_hours));
          setServiceCount(data.service_count ? String(data.service_count) : '');
          setServiceContent(data.service_content || '');
        } catch (err) {
          console.error(err);
          alert('데이터를 불러오지 못했습니다.');
        } finally {
          setLoading(false);
        }
      };
      fetchLog();
    }
  }, [id, isEditMode]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!assignmentId || !serviceDate || !serviceHours) {
      alert('배정 ID, 서비스 날짜, 제공 시간은 필수 입력값입니다.');
      return;
    }

    try {
      if (isEditMode) {
        await updateServiceLog(Number(id), {
          service_date: serviceDate,
          service_hours: Number(serviceHours),
          service_count: serviceCount ? Number(serviceCount) : null,
          service_content: serviceContent || null,
        });
        alert('성공적으로 수정되었습니다.');
      } else {
        await createServiceLog({
          assignment_id: Number(assignmentId),
          service_date: serviceDate,
          service_hours: Number(serviceHours),
          service_count: serviceCount ? Number(serviceCount) : null,
          service_content: serviceContent || null,
        });
        alert('성공적으로 등록되었습니다.');
      }
      navigate('/service-logs');
    } catch (err) {
      console.error(err);
      const detail = axios.isAxiosError(err) ? err.response?.data?.detail : undefined;
      alert(typeof detail === 'string' ? detail : '저장 실패: 서버 에러 또는 유효하지 않은 데이터입니다.');
    }
  };

  if (loading) return <div className="loading-box">로딩 중... 🚀</div>;

  return (
    <div className="servicelog-container">
      <div className="form-card">
        <h2>{isEditMode ? '📝 이용내역 수정' : '📝 신규 이용내역 등록'}</h2>
        <form onSubmit={handleSubmit} className="servicelog-form">
          <div className="form-group">
            <label>배정 ID (assignment_id) *</label>
            <input 
              type="number" 
              placeholder="배정 번호" 
              value={assignmentId} 
              onChange={(e) => setAssignmentId(e.target.value)} 
              disabled={isEditMode} // 수정 시에는 배정 ID 변경 불가
            />
          </div>
          <div className="form-group">
            <label>서비스 제공일 *</label>
            <input 
              type="date" 
              value={serviceDate} 
              onChange={(e) => setServiceDate(e.target.value)} 
            />
          </div>
          <div className="form-group">
            <label>제공 시간 (시간) *</label>
            <input 
              type="number" 
              step="0.1" 
              placeholder="예: 3.5" 
              value={serviceHours} 
              onChange={(e) => setServiceHours(e.target.value)} 
            />
          </div>
          <div className="form-group">
            <label>제공 횟수</label>
            <input 
              type="number" 
              placeholder="옵션" 
              value={serviceCount} 
              onChange={(e) => setServiceCount(e.target.value)} 
            />
          </div>
          <div className="form-group">
            <label>주요 서비스 수행 내용</label>
            <textarea 
              placeholder="옵션" 
              value={serviceContent} 
              onChange={(e) => setServiceContent(e.target.value)}
              rows={4}
            />
          </div>
          <div className="form-actions">
            <button type="button" className="btn-secondary" onClick={() => navigate('/service-logs')}>취소</button>
            <button type="submit" className="btn-primary">{isEditMode ? '수정하기' : '등록하기'}</button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ServiceLogForm;