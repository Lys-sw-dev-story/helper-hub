import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { getAssistants, type AssistantDetail } from '../../api/assistantApi';
import './Assistant.css';

const AssistantList: React.FC = () => {
  const [assistants, setAssistants] = useState<AssistantDetail[]>([]);
  const navigate = useNavigate();

  const orgName = localStorage.getItem('organization_name');

  useEffect(() => {
    getAssistants().then(setAssistants).catch(console.error);
  }, []);

  return (
    <div className="assistant-card">
      <div className="page-header">
        <h2>🤝 활동지원사 관리 목록</h2>
        <Link to="/assistants/register">
          <button className="btn btn-primary">+ 신규 등록</button>
        </Link>
      </div>
      
      <table className="assistant-table">
        <thead>
          <tr>
            <th>성함</th>
            <th>소속 기관</th>
            <th style={{ textAlign: 'right' }}>관리</th>
          </tr>
        </thead>
        <tbody>
          {assistants.length === 0 ? (
            <tr>
              <td colSpan={3} style={{ textAlign: 'center', padding: '3rem', color: '#888' }}>
                등록된 활동지원사가 없습니다.
              </td>
            </tr>
          ) : (
            assistants.map((ast) => (
              <tr key={ast.assistant_id}>
                <td style={{ fontWeight: '600' }}>{ast.assistant_name}</td>
                <td>{orgName}</td>
                <td style={{ textAlign: 'right' }}>
                  <button className="btn btn-primary" onClick={() => navigate(`/assistants/${ast.assistant_id}`)}>
                    자세히 보기 🔍
                  </button>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
};

export default AssistantList;