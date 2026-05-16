import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getAssistants } from '../../api/assistantApi';
import './AssistantList.css';

const AssistantList: React.FC = () => {
  const [assistants, setAssistants] = useState<any[]>([]);

  useEffect(() => {
    getAssistants().then(setAssistants).catch(console.error);
  }, []);

  return (
    <div className="assistant-list-container">
      <div className="list-header">
        <h2>🤝 활동지원사 관리 목록</h2>
        <Link to="/assistants/register">
          <button className="register-btn">+ 신규 활동지원사</button>
        </Link>
      </div>
      <table className="assistant-table">
        <thead>
          <tr>
            <th>성함</th>
            <th>연락처</th>
            <th>근무 가능 요일</th>
            <th>업무 시작일</th>
            <th>자격증</th>
          </tr>
        </thead>
        <tbody>
          {assistants.map((ast) => (
            <tr key={ast.assistant_id}>
              <td style={{ padding: '10px' }}>{ast.assistant_name}</td>
              <td>{ast.assistant_phone || '-'}</td>
              <td>{ast.work_days || '-'}</td>
              <td>{ast.work_start_date || '-'}</td>
              <td>{ast.assistant_license || '-'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AssistantList;