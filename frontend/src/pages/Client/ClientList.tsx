import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getClients } from '../../api/clientApi';
import './ClientList.css';

const ClientList: React.FC = () => {
  const [clients, setClients] = useState<any[]>([]);

  useEffect(() => {
    getClients().then(setClients).catch(console.error);
  }, []);

  return (
    <div className="client-list-container">
      <div className="list-header">
        <h2>이용자 관리 목록</h2>
        <Link to="/clients/register">
          <button className="register-btn">+ 신규 등록</button>
        </Link>
      </div>
      <table className="client-table">
        <thead>
          <tr>
            <th>성함</th>
            <th>생년월일</th>
            <th>연락처</th>
            <th>상태</th>
            <th>주소</th>
          </tr>
        </thead>
        <tbody>
          {clients.map((client) => (
            <tr key={client.client_id}>
              <td>{client.client_name}</td>
              <td>{client.client_birth_date || '-'}</td>
              <td>{client.client_phone || '-'}</td>
              <td>
                <span className={`status-badge ${client.client_status === '대기' ? 'waiting' : 'active'}`}>
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