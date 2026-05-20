import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { createAssignment } from '../../api/assignmentApi';
import './Assignment.css';

const AssignmentForm: React.FC = () => {
  const navigate = useNavigate();
  const [staffId, setStaffId] = useState('');
  const [clientId, setClientId] = useState('');
  const [assistantId, setAssistantId] = useState('');
  const [startDate, setStartDate] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!staffId || !clientId || !assistantId || !startDate) {
      alert('모든 필수 항목을 입력해 주세요.');
      return;
    }

    try {
      await createAssignment({
        staff_id: Number(staffId),
        client_id: Number(clientId),
        assistant_id: Number(assistantId),
        start_date: startDate,
        end_date: null
      });
      alert('🤝 매칭 배정이 성공적으로 데이터베이스에 등록되었습니다!');
      navigate('/assignments');
    } catch (err) {
      console.error(err);
      const detail = axios.isAxiosError(err) ? err.response?.data?.detail : undefined;
      alert(typeof detail === 'string' ? detail : '등록 실패: 서버 에러 또는 유효하지 않은 FK 데이터입니다.');
    }
  };

  return (
    <div className="assignment-form-container">
      <div className="form-card">
        <h2>🤝 신규 매칭 배정 등록</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>담당 직원 ID (staff_id) *</label>
            <input type="number" placeholder="직원 번호" value={staffId} onChange={(e) => setStaffId(e.target.value)} />
          </div>
          <div className="form-group">
            <label>이용자 고유 ID (client_id) *</label>
            <input type="number" placeholder="이용자 번호" value={clientId} onChange={(e) => setClientId(e.target.value)} />
          </div>
          <div className="form-group">
            <label>활동지원사 고유 ID (assistant_id) *</label>
            <input type="number" placeholder="활동지원사 번호" value={assistantId} onChange={(e) => setAssistantId(e.target.value)} />
          </div>
          <div className="form-group">
            <label>배정 시작일 (start_date) *</label>
            <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
          </div>
          <div className="form-actions">
            <button type="submit" className="btn btn-primary btn-block">매칭 등록하기 🔗</button>
            <button type="button" className="btn btn-secondary btn-block" onClick={() => navigate('/assignments')}>취소</button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AssignmentForm;