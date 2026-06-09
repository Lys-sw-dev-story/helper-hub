import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { deleteClient, getClients, type ClientDetail } from '../../api/clientApi';
import './Client.css';

const ClientList: React.FC = () => {
  const navigate = useNavigate();
  const [clients, setClients] = useState<ClientDetail[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchClients = async () => {
    try {
      setLoading(true);
      const data = await getClients();
      console.log('이용자 목록 조회 결과:', data);
      setClients(data);
    } catch (error) {
      console.error('이용자 목록 조회 실패:', error);
      setClients([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchClients();
  }, []);

  const handleDelete = async (clientId: number) => {
    const confirmed = window.confirm('정말 삭제하시겠습니까?');

    if (!confirmed) return;

    try {
      await deleteClient(clientId);
      alert('이용자가 삭제되었습니다.');
      fetchClients();
    } catch (error) {
      console.error('이용자 삭제 실패:', error);
      const detail = axios.isAxiosError(error) ? error.response?.data?.detail : undefined;
      alert(typeof detail === 'string' ? detail : '삭제 실패! 다시 시도해 주세요.');
    }
  };

  return (
    <div className="client-card">
      <div className="page-header">
        <h2>👵 이용자 관리 목록</h2>
        <button
          type="button"
          className="btn btn-primary"
          onClick={() => navigate('/clients/register')}
        >
          + 신규 등록
        </button>
      </div>

      <table className="client-table">
        <thead>
          <tr>
            <th>성함</th>
            <th>소속 기관</th>
            <th>현재 상태</th>
            <th>관리</th>
          </tr>
        </thead>

        <tbody>
          {loading ? (
            <tr>
              <td colSpan={4}>불러오는 중입니다...</td>
            </tr>
          ) : clients.length === 0 ? (
            <tr>
              <td colSpan={4}>등록된 이용자가 없습니다.</td>
            </tr>
          ) : (
            clients.map((client) => (
              <tr key={client.client_id}>
                <td>{client.client_name}</td>
                <td>{client.organization_id ? `기관 #${client.organization_id}` : '-'}</td>
                <td>{client.client_status || '-'}</td>
                <td>
                  <button
                    type="button"
                    className="btn btn-secondary"
                    onClick={() => navigate(`/clients/${client.client_id}`)}
                  >
                    상세
                  </button>

                  <button
                    type="button"
                    className="btn btn-secondary"
                    onClick={() => navigate(`/clients/${client.client_id}/edit`)}
                  >
                    수정
                  </button>

                  <button
                    type="button"
                    className="btn btn-danger"
                    onClick={() => handleDelete(client.client_id)}
                  >
                    삭제
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