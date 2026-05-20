import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { registerClient, type ClientData } from '../../api/clientApi';
import './Client.css';

const ClientRegister: React.FC = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<ClientData>({
    client_name: '', client_birth_date: '', client_phone: '',
    client_address: '', client_status: '대기', client_memo: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const submitData = { ...formData };
      if (!submitData.client_birth_date) delete submitData.client_birth_date;

      await registerClient(submitData);
      alert('이용자가 정상적으로 등록되었습니다! 🎉');
      navigate('/clients');
    } catch (err) {
      console.error(err);
      alert('등록 실패! 다시 시도해 주세요.');
    }
  };

  return (
    <div className="client-card">
      <div className="page-header">
        <h2>👵 신규 이용자 등록</h2>
      </div>

      <form onSubmit={handleSubmit} className="client-form">
        <div className="form-group">
          <label>이용자 성함 (필수)</label>
          <input name="client_name" placeholder="이름 입력" onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>생년월일</label>
          <input name="client_birth_date" type="date" onChange={handleChange} />
        </div>
        <div className="form-group">
          <label>연락처</label>
          <input name="client_phone" placeholder="010-0000-0000" onChange={handleChange} />
        </div>
        <div className="form-group">
          <label>거주지 주소</label>
          <input name="client_address" placeholder="주소 입력" onChange={handleChange} />
        </div>
        <div className="form-group">
          <label>현재 상태</label>
          <select name="client_status" onChange={handleChange} defaultValue="대기">
            <option value="대기">대기</option>
            <option value="매칭중">매칭 중</option>
            <option value="이용중">이용 중</option>
            <option value="종료">종료</option>
          </select>
        </div>
        <div className="form-group">
          <label>메모 및 특이사항</label>
          <textarea name="client_memo" placeholder="상세 비고 내용 입력" onChange={handleChange} rows={4} />
        </div>

        <div className="btn-group">
          <button type="submit" className="btn btn-success" style={{ flex: 1 }}>등록 완료 💾</button>
          <button type="button" className="btn btn-secondary" style={{ flex: 1 }} onClick={() => navigate('/clients')}>취소</button>
        </div>
      </form>
    </div>
  );
};

export default ClientRegister;