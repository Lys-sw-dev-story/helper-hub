import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { getAssignmentById, endAssignment, type Assignment } from '../../api/assignmentApi';
import './Assignment.css';

const AssignmentDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [assignment, setAssignment] = useState<Assignment | null>(null);
  const [endDateInput, setEndDateInput] = useState<string>('');
  const [isEnding, setIsEnding] = useState<boolean>(false);

  useEffect(() => {
    if (id) {
      getAssignmentById(Number(id))
        .then(setAssignment)
        .catch((err) => {
          console.error(err);
          alert('해당 매칭 정보를 찾을 수 없습니다.');
          navigate('/assignments');
        });
    }
  }, [id, navigate]);

  const handleEndSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!id || !endDateInput) {
      alert('종료일을 입력해 주세요.');
      return;
    }

    try {
      await endAssignment(Number(id), endDateInput);
      alert('🔒 해당 매칭 계약이 정상적으로 종료 처리되었습니다.');
      setIsEnding(false);
      const updated = await getAssignmentById(Number(id));
      setAssignment(updated);
    } catch (err) {
      console.error(err);
      alert('종료 처리 중 서버 오류가 발생했습니다.');
    }
  };

  if (!assignment) return <div className="loading-box">상세 데이터를 가져오는 중...</div>;

  const clientDisplay = assignment.client_name || '고객';
  const assistantDisplay = assignment.assistant_name || '지원사';

  return (
    <div className="assignment-detail-container">
      <div className="detail-card">
        <div className="detail-header-section">
          {/* 💡 타이틀 가독성 극대화: 이름으로만 매칭 관계 직관적 표시 */}
          <h2>🔍 {clientDisplay} ↔ {assistantDisplay} 매칭 상세</h2>
          <button className="btn btn-secondary" onClick={() => navigate('/assignments')}>목록으로</button>
        </div>

        <div className="detail-content-grid">
          <div className="detail-info-block flex-row-status">
            <h3>매칭 관리 상태:</h3>
            <span className={`status-tag ${assignment.assignment_status}`}>
              {assignment.assignment_status === 'active' ? '매칭중' : '매칭종료'}
            </span>
          </div>

          <div className="detail-info-cards-container">
            {/* 💡 이용자 정보 카드 클릭 -> 해당 이용자 상세페이지 워프 */}
            <Link to={`/clients/${assignment.client_id}`} className="info-sub-card link-card">
              <span className="card-badge client-label">이용자 상세 바로가기 ↗</span>
              <h3 className="card-main-name">{assignment.client_name || '이름 정보 없음'}</h3>
              <p className="card-click-hint">클릭 시 이용자 프로필로 이동</p>
            </Link>

            {/* 💡 활동지원사 정보 카드 클릭 -> 해당 활동지원사 상세페이지 워프 */}
            <Link to={`/assistants/${assignment.assistant_id}`} className="info-sub-card link-card">
              <span className="card-badge assistant-label">활동지원사 상세 바로가기 ↗</span>
              <h3 className="card-main-name">{assignment.assistant_name || '이름 정보 없음'}</h3>
              <p className="card-click-hint">클릭 시 활동지원사 프로필로 이동</p>
            </Link>
          </div>

          <div className="detail-info-block spec-info-zone">
            <h3>📅 계약 일정 및 내부 식별 시스템</h3>
            <div className="spec-table">
              <p><strong>배정 시작일:</strong> {assignment.start_date}</p>
              <p><strong>배정 종료일:</strong> {assignment.end_date || <span className="text-active">현재 서비스 제공 중 (NULL)</span>}</p>
              <p><strong>담당 매니저 ID (staff_id):</strong> {assignment.staff_id}</p>
              <p><strong>배정 일련번호 (assignment_id):</strong> {assignment.assignment_id}</p>
            </div>
          </div>
        </div>

        {assignment.assignment_status === 'active' && (
          <div className="detail-actions-zone">
            {!isEnding ? (
              <button className="btn btn-danger" onClick={() => setIsEnding(true)}>배정 종료하기</button>
            ) : (
              <form onSubmit={handleEndSubmit} className="end-inline-form">
                <label> 배정 종료일 선택:</label>
                <input 
                  type="date" 
                  value={endDateInput} 
                  onChange={(e) => setEndDateInput(e.target.value)} 
                  required
                />
                <button type="submit" className="btn btn-danger">종료 확정</button>
                <button type="button" className="btn btn-secondary" onClick={() => setIsEnding(false)}>취소</button>
              </form>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default AssignmentDetail;