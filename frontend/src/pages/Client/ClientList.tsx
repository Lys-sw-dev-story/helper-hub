import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { getClients, type ClientDetail } from '../../api/clientApi';
import './Client.css';

const ClientList: React.FC = () => {
  const [clients, setClients] = useState<ClientDetail[]>([]);
  const navigate = useNavigate();

  const orgName = localStorage.getItem('organization_name') || '우리 복지관';

  useEffect(() => {
    getClients().then(setClients).catch(console.error);
  }, []);

  return (
    <div className="client-card">
      <div className="page-header">
        <h2>👵 이용자 관리 목록</h2>
        <Link to="/clients/register">
          <button className="btn btn-primary">+ 신규 등록</button>
        </Link>
      </div>
      
      <table className="client-table">
        <thead>
          <tr>
            <th>성함</th>
            <th>소속 기관</th>
            <th>현재 상태</th>
            <th style={{ textAlign: 'right' }}>관리</th>
          </tr>
        </thead>
        <tbody>
          {clients.length === 0 ? (
            <tr>
              <td colSpan={4} style={{ textAlign: 'center', padding: '3rem', color: '#888' }}>
                등록된 이용자가 없습니다.
              </td>
            </tr>
          ) : (
            clients.map((client) => (
              <tr key={client.client_id}>
                <td style={{ fontWeight: '600' }}>{client.client_name}</td>
                <td>{orgName}</td>
                <td>
                  <span className={`status-badge ${client.client_status || '대기'}`}>
                    {client.client_status || '대기'}
                  </span>
                </td>
                <td style={{ textAlign: 'right' }}>
                  <button className="btn btn-primary" onClick={() => navigate(`/clients/${client.client_id}`)}>
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

export default ClientList;