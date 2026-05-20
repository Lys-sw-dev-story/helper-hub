import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { getAssignments, type Assignment } from '../../api/assignmentApi';
import './Assignment.css';

const AssignmentList: React.FC = () => {
  const navigate = useNavigate();
  const [assignments, setAssignments] = useState<Assignment[]>([]);
  const [filter, setFilter] = useState<'all' | 'active' | 'ended'>('all');
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    getAssignments()
      .then(setAssignments)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const filteredAssignments = assignments.filter((item) => {
    if (filter === 'active') return item.assignment_status === 'active';
    if (filter === 'ended') return item.assignment_status === 'ended';
    return true;
  });

  if (loading) return <div className="loading-box">매칭 데이터를 불러오는 중...</div>;

  return (
    <div className="assignment-container">
      <div className="page-header">
        <h2>🤝 매칭 및 배정 관리</h2>
        <Link to="/assignments/new">
          <button className="btn btn-primary">+ 신규 배정 등록</button>
        </Link>
      </div>

      {/* 필터링 탭 구역 */}
      <div className="filter-tab-bar">
        <button className={`filter-tab ${filter === 'all' ? 'active' : ''}`} onClick={() => setFilter('all')}>
          전체 ({assignments.length})
        </button>
        <button className={`filter-tab ${filter === 'active' ? 'active' : ''}`} onClick={() => setFilter('active')}>
          매칭중 ({assignments.filter(a => a.assignment_status === 'active').length})
        </button>
        <button className={`filter-tab ${filter === 'ended' ? 'active' : ''}`} onClick={() => setFilter('ended')}>
          매칭종료 ({assignments.filter(a => a.assignment_status === 'ended').length})
        </button>
      </div>

      <div className="assignment-card">
        <table className="assignment-table">
          <thead>
            <tr>
              <th>이용자명 (고객)</th>
              <th>활동지원사명</th>
              <th>배정 시작일</th>
              <th>매칭 상태</th>
            </tr>
          </thead>
          <tbody>
            {filteredAssignments.length === 0 ? (
              <tr><td colSpan={4} className="empty-row">해당하는 매칭 내역이 없습니다.</td></tr>
            ) : (
              filteredAssignments.map((asm) => (
                <tr 
                  key={asm.assignment_id} 
                  className="clickable-row"
                  onClick={() => navigate(`/assignments/${asm.assignment_id}`)}
                >
                  <td className="emp-name">
                    {asm.client_name || `고객 (ID: ${asm.client_id})`}
                  </td>
                  <td className="assistant-name-cell">
                    {asm.assistant_name || `지원사 (ID: ${asm.assistant_id})`}
                  </td>
                  <td>{asm.start_date}</td>
                  <td>
                    <span className={`status-tag ${asm.assignment_status}`}>
                      {asm.assignment_status === 'active' ? '매칭중' : '매칭종료'}
                    </span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default AssignmentList;