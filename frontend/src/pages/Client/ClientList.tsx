import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getClients } from '../../api/clientApi';

const ClientList: React.FC = () => {
  const [clients, setClients] = useState<any[]>([]);

  useEffect(() => {
    getClients().then(setClients).catch(console.error);
  }, []);

  return (
    <div style={{ padding: '2rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>이용자 관리 목록</h2>
        <Link to="/clients/register">
          <button style={{ padding: '0.5rem 1rem', cursor: 'pointer' }}>+ 신규 등록</button>
        </Link>
      </div>
      <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '1rem' }}>
        <thead>
          <tr style={{ borderBottom: '2px solid #333', textAlign: 'left' }}>
            <th style={{ padding: '10px' }}>성함</th>
            <th>생년월일</th>
            <th>연락처</th>
            <th>상태</th>
            <th>주소</th>
          </tr>
        </thead>
        <tbody>
          {clients.map((client) => (
            <tr key={client.client_id} style={{ borderBottom: '1px solid #ddd' }}>
              <td style={{ padding: '10px' }}>{client.client_name}</td>
              <td>{client.client_birth_date || '-'}</td>
              <td>{client.client_phone || '-'}</td>
              <td>
                <span style={{ 
                  padding: '4px 8px', 
                  borderRadius: '4px', 
                  backgroundColor: client.client_status === '대기' ? '#eee' : '#e3f2fd' 
                }}>
                  {client.client_status || '대기'}
                </span>
              </td>
              <td>{client.client_address || '-'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ClientList;