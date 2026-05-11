import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getAssistants } from '../../api/assistantApi';

const AssistantList: React.FC = () => {
  const [assistants, setAssistants] = useState<any[]>([]);

  useEffect(() => {
    getAssistants().then(setAssistants).catch(console.error);
  }, []);

  return (
    <div style={{ padding: '2rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>🤝 조력자 관리 목록</h2>
        <Link to="/assistants/register">
          <button style={{ padding: '0.5rem 1rem', cursor: 'pointer' }}>+ 신규 조력자</button>
        </Link>
      </div>
      <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '1rem' }}>
        <thead>
          <tr style={{ borderBottom: '2px solid #333', textAlign: 'left' }}>
            <th style={{ padding: '10px' }}>성함</th>
            <th>연락처</th>
            <th>근무 가능 요일</th>
            <th>업무 시작일</th>
            <th>자격증</th>
          </tr>
        </thead>
        <tbody>
          {assistants.map((ast) => (
            <tr key={ast.assistant_id} style={{ borderBottom: '1px solid #ddd' }}>
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