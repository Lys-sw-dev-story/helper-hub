import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { registerClient, type ClientData } from '../../api/clientApi';
import { TagSelector } from '../../components/common/Tags';
import { WEEKDAYS, SUPPORT_TYPES } from '../../lib/constants';
import './Client.css';

const ClientRegister: React.FC = () => {
  const navigate = useNavigate();

  const [formData, setFormData] = useState<Omit<ClientData, 'organization_id'>>({
    client_name: '',
    client_birth_date: '',
    client_phone: '',
    client_address: '',
    client_status: '대기',
    client_memo: '',
    client_preferred_days: '',
    client_support_types: '',
  });

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const setTag = (name: keyof ClientData) => (csv: string) => {
    setFormData((prev) => ({ ...prev, [name]: csv }));
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    try {
      // 🔥 [해결책] 로컬 스토리지 등에 저장된 로그인 유저 정보에서 organization_id를 동적으로 가져옴
      // 만약 세션 저장 키 이름이 다르면 'user'나 'staff' 등으로 맞춰줘!
      const storedUser = localStorage.getItem('user');
      const userObj = storedUser ? JSON.parse(storedUser) : null;
      const currentOrgId = userObj?.organization_id || 1; // 정 안되면 기본값 1

      const submitData: ClientData = {
        client_name: formData.client_name,
        client_birth_date: formData.client_birth_date || undefined,
        client_phone: formData.client_phone || undefined,
        client_address: formData.client_address || undefined,
        client_status: formData.client_status || undefined,
        client_memo: formData.client_memo || undefined,
        client_preferred_days: formData.client_preferred_days || undefined,
        client_support_types: formData.client_support_types || undefined,
        organization_id: currentOrgId, // 🔐 하드코딩 1 대신 현재 로그인한 기관 ID 동적 주입!
      };

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
          <label htmlFor="client_name">이용자 성함 (필수)</label>
          <input
            id="client_name"
            name="client_name"
            placeholder="이름 입력"
            value={formData.client_name}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="client_birth_date">생년월일</label>
          <input id="client_birth_date" name="client_birth_date" type="date" value={formData.client_birth_date} onChange={handleChange} />
        </div>

        <div className="form-group">
          <label htmlFor="client_phone">연락처</label>
          <input id="client_phone" name="client_phone" placeholder="010-0000-0000" value={formData.client_phone} onChange={handleChange} />
        </div>

        <div className="form-group">
          <label htmlFor="client_address">거주지 주소</label>
          <input id="client_address" name="client_address" placeholder="주소 입력" value={formData.client_address} onChange={handleChange} />
        </div>

        <div className="form-group">
          <label htmlFor="client_status">현재 상태</label>
          <select id="client_status" name="client_status" value={formData.client_status} onChange={handleChange}>
            <option value="대기">대기</option>
            <option value="매칭 중">매칭 중</option>
            <option value="이용 중">이용 중</option>
            <option value="종료">종료</option>
          </select>
        </div>

        <div className="form-group">
          <label>희망 요일 (매칭 태그)</label>
          <TagSelector
            options={WEEKDAYS}
            value={formData.client_preferred_days}
            onChange={setTag('client_preferred_days')}
            variant="day"
          />
        </div>

        <div className="form-group">
          <label>희망 지원 분야 (매칭 태그)</label>
          <TagSelector
            options={SUPPORT_TYPES}
            value={formData.client_support_types}
            onChange={setTag('client_support_types')}
            variant="support"
          />
        </div>

        <div className="form-group">
          <label htmlFor="client_memo">메모 및 특이사항</label>
          <textarea id="client_memo" name="client_memo" placeholder="상세 비고 내용 입력" value={formData.client_memo} onChange={handleChange} rows={4} />
        </div>

        <div className="btn-group" style={{ marginTop: '2rem' }}>
          <button type="submit" className="btn btn-success" style={{ flex: 1 }}>등록 완료 💾</button>
          <button type="button" className="btn btn-secondary" style={{ flex: 1 }} onClick={() => navigate('/clients')}>취소</button>
        </div>
      </form>
    </div>
  );
};

export default ClientRegister;