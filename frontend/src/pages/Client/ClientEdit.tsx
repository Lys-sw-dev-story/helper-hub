import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getClient, updateClient, type ClientData } from '../../api/clientApi';
import './Client.css';

const ClientEdit: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const clientId = Number(id);

  const [loading, setLoading] = useState(true);
  const [formData, setFormData] = useState<ClientData>({
    client_name: '', client_birth_date: '', client_phone: '',
    client_address: '', client_status: '대기', client_memo: '',
  });

  useEffect(() => {
    if (clientId) {
      getClient(clientId)
        .then((data) => {
          setFormData({
            client_name: data.client_name,
            client_phone: data.client_phone || '',
            client_birth_date: data.client_birth_date || '',
            client_address: data.client_address || '',
            client_status: data.client_status || '대기',
            client_memo: data.client_memo || '',
          });
          setLoading(false);
        })
        .catch((err) => {
          console.error(err);
          alert('데이터를 가져오는 데 실패했습니다.');
          navigate('/clients');
        });
    }
  }, [clientId, navigate]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await updateClient(clientId, formData);
      alert('이용자 정보가 성공적으로 수정되었습니다! 💾');
      navigate(`/clients/${clientId}`);
    } catch (err) {
      console.error(err);
      alert('정보 수정에 실패했습니다.');
    }
  };

  if (loading) return <div style={{ textAlign: 'center', padding: '3rem' }}>기존 데이터를 세팅 중...</div>;

  return (
    <div className="client-card">
      <div className="page-header">
        <h2>📝 이용자 프로필 수정</h2>
      </div>

      <form onSubmit={handleSubmit} className="client-form">
        <div className="form-group">
          <label>이용자 성함 (필수)</label>
          <input name="client_name" value={formData.client_name} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>생년월일</label>
          <input name="client_birth_date" type="date" value={formData.client_birth_date} onChange={handleChange} />
        </div>
        <div className="form-group">
          <label>연락처</label>
          <input name="client_phone" value={formData.client_phone} onChange={handleChange} />
        </div>
        <div className="form-group">
          <label>거주지 주소</label>
          <input name="client_address" value={formData.client_address} onChange={handleChange} />
        </div>
        <div className="form-group">
          <label>현재 상태</label>
          <select name="client_status" value={formData.client_status} onChange={handleChange}>
            <option value="대기">대기</option>
            <option value="매칭중">매칭 중</option>
            <option value="이용중">이용 중</option>
            <option value="종료">종료</option>
          </select>
        </div>
        <div className="form-group">
          <label>메모 및 특이사항</label>
          <textarea name="client_memo" value={formData.client_memo} onChange={handleChange} rows={4} />
        </div>

        <div className="btn-group">
          <button type="submit" className="btn btn-primary" style={{ flex: 1 }}>변경사항 저장 💾</button>
          <button type="button" className="btn btn-secondary" style={{ flex: 1 }} onClick={() => navigate(`/clients/${clientId}`)}>수정 취소</button>
        </div>
      </form>
    </div>
  );
};

export default ClientEdit;