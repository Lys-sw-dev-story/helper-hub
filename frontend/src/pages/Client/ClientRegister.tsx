import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { registerClient, type ClientData } from '../../api/clientApi';
import './ClientRegister.css';

const ClientRegister: React.FC = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<ClientData>({
    client_name: '', client_birth_date: '', client_phone: '',
    client_address: '', client_status: '대기', client_memo: '',
    organization_id: 1,
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const submitData = { ...formData, 
        client_birth_date: formData.client_birth_date || null,
        client_phone: formData.client_phone || null,
        client_address: formData.client_address || null,
        client_memo: formData.client_memo || null,
      };
      await registerClient(submitData);
      alert('이용자가 성공적으로 등록되었습니다!');
      navigate('/clients');
    } catch (err) {
      alert('등록 실패!');
    }
  };

  return (
    <div className="register-container">
      <h2>👵 이용자 신규 등록</h2>
      <form onSubmit={handleSubmit} className="register-form">
        <div className="input-group">
          <label>성함</label>
          <input name="client_name" className="form-input" placeholder="이용자 이름" onChange={handleChange} required />
        </div>
        <div className="input-group">
          <label>생년월일</label>
          <input name="client_birth_date" type="date" className="form-input" onChange={handleChange} />
        </div>
        <div className="input-group">
          <label>연락처</label>
          <input name="client_phone" className="form-input" placeholder="010-0000-0000" onChange={handleChange} />
        </div>
        <div className="input-group">
          <label>주소</label>
          <input name="client_address" className="form-input" placeholder="거주지 주소" onChange={handleChange} />
        </div>
        <div className="input-group">
          <label>현재 상태</label>
          <select name="client_status" className="form-input" onChange={handleChange}>
            <option value="대기">대기</option>
            <option value="매칭중">매칭 중</option>
            <option value="이용중">이용 중</option>
            <option value="종료">종료</option>
          </select>
        </div>
        <div className="input-group">
          <label>메모 및 특이사항</label>
          <textarea name="client_memo" className="form-input" placeholder="비고" onChange={handleChange} rows={4} />
        </div>
        <button type="submit" className="submit-btn">등록하기</button>
      </form>
    </div>
  );
};

export default ClientRegister;