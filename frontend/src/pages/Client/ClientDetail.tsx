import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { getClient, deleteClient, type ClientData } from '../../api/clientApi';
import DocumentSection from '../../components/common/DocumentSection';
import { DocumentTargetType } from '../../api/documentApi';
import { TagChips } from '../../components/common/Tags';
import './Client.css';

const ClientDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const clientId = Number(id);

  const [loading, setLoading] = useState(true);
  const [data, setData] = useState<ClientData | null>(null);

  useEffect(() => {
    let ignore = false;
    if (clientId) {
      getClient(clientId)
        .then((res) => {
          if (ignore) return;
          setData(res);
          setLoading(false);
        })
        .catch((err) => {
          if (ignore) return;
          console.error(err);
          const detail = axios.isAxiosError(err) ? err.response?.data?.detail : undefined;
          alert(typeof detail === 'string' ? detail : '데이터를 가져오지 못했습니다.');
          navigate('/clients');
        });
    }
    return () => {
      ignore = true;
    };
  }, [clientId, navigate]);

  const handleDelete = async () => {
    if (window.confirm('정말로 이 이용자 정보를 완전히 삭제하시겠습니까?')) {
      try {
        await deleteClient(clientId);
        alert('이용자 정보가 성공적으로 삭제되었습니다.');
        navigate('/clients');
      } catch (err) {
        console.error(err);
        const detail = axios.isAxiosError(err) ? err.response?.data?.detail : undefined;
        alert(typeof detail === 'string' ? detail : '삭제에 실패했습니다.');
      }
    }
  };

  if (loading) return <div style={{ textAlign: 'center', padding: '3rem' }}>정보를 불러오는 중...</div>;
  if (!data) return <div style={{ textAlign: 'center', padding: '3rem' }}>데이터가 존재하지 않습니다.</div>;

  return (
    <div className="client-card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <h2>🔍 이용자 상세 프로필</h2>
        <button onClick={handleDelete} className="btn btn-danger">정보 삭제 🗑️</button>
      </div>

      <div className="client-form">
        <div className="form-group">
          <label>성함</label>
          <div className="detail-value" style={{ fontWeight: 'bold' }}>{data.client_name}</div>
        </div>
        <div className="form-group">
          <label>생년월일</label>
          <div className="detail-value">{data.client_birth_date || '-'}</div>
        </div>
        <div className="form-group">
          <label>연락처</label>
          <div className="detail-value">{data.client_phone || '-'}</div>
        </div>
        <div className="form-group">
          <label>주소</label>
          <div className="detail-value">{data.client_address || '-'}</div>
        </div>
        <div className="form-group">
          <label>현재 매칭 상태</label>
          <div>
            <span className={`status-badge ${data.client_status || '대기'}`}>
              {data.client_status || '대기'}
            </span>
          </div>
        </div>
        <div className="form-group">
          <label>희망 요일 (매칭 태그)</label>
          <div className="detail-value">
            <TagChips tags={data.client_preferred_days} variant="day" emptyText="등록된 희망 요일이 없습니다." />
          </div>
        </div>
        <div className="form-group">
          <label>희망 지원 분야 (매칭 태그)</label>
          <div className="detail-value">
            <TagChips tags={data.client_support_types} variant="support" emptyText="등록된 희망 지원 분야가 없습니다." />
          </div>
        </div>
        <div className="form-group">
          <label>메모 및 특이사항</label>
          <div className="detail-value memo">{data.client_memo || '등록된 특이사항이 없습니다.'}</div>
        </div>

        <DocumentSection targetType={DocumentTargetType.CLIENT} targetId={clientId} readOnly={true} />

        <div className="btn-group" style={{ marginTop: '2rem' }}>
          <button type="button" className="btn btn-primary" style={{ flex: 1 }} onClick={() => navigate(`/clients/${clientId}/edit`)}>
            정보 수정하러 가기 ✏️
          </button>
          <button type="button" className="btn btn-secondary" style={{ flex: 1 }} onClick={() => navigate('/clients')}>
            목록으로 돌아가기
          </button>
        </div>
      </div>
    </div>
  );
};

export default ClientDetail;