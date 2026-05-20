import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { registerClient, type ClientData } from '../../api/clientApi';
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
  });

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    try {
      const submitData: ClientData = {
        client_name: formData.client_name,
        client_birth_date: formData.client_birth_date || undefined,
        client_phone: formData.client_phone || undefined,
        client_address: formData.client_address || undefined,
        client_status: formData.client_status || undefined,
        client_memo: formData.client_memo || undefined,

        // seed_staff.py에서 생성된 organization id가 1이었기 때문에 데모용으로 고정
        organization_id: 1,
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
          <input
            id="client_birth_date"
            name="client_birth_date"
            type="date"
            value={formData.client_birth_date}
            onChange={handleChange}
          />
        </div>

        <div className="form-group">
          <label htmlFor="client_phone">연락처</label>
          <input
            id="client_phone"
            name="client_phone"
            placeholder="010-0000-0000"
            value={formData.client_phone}
            onChange={handleChange}
          />
        </div>

        <div className="form-group">
          <label htmlFor="client_address">거주지 주소</label>
          <input
            id="client_address"
            name="client_address"
            placeholder="주소 입력"
            value={formData.client_address}
            onChange={handleChange}
          />
        </div>

        <div className="form-group">
          <label htmlFor="client_status">현재 상태</label>
          <select
            id="client_status"
            name="client_status"
            value={formData.client_status}
            onChange={handleChange}
          >
            <option value="대기">대기</option>
            <option value="매칭 중">매칭 중</option>
            <option value="이용 중">이용 중</option>
            <option value="종료">종료</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="client_memo">메모 및 특이사항</label>
          <textarea
            id="client_memo"
            name="client_memo"
            placeholder="상세 비고 내용 입력"
            value={formData.client_memo}
            onChange={handleChange}
            rows={4}
          />
        </div>

        <div className="btn-group">
          <button type="submit" className="btn btn-success" style={{ flex: 1 }}>
            등록 완료 💾
          </button>

          <button
            type="button"
            className="btn btn-secondary"
            style={{ flex: 1 }}
            onClick={() => navigate('/clients')}
          >
            취소
          </button>
        </div>
      </form>
    </div>
  );
};

export default ClientRegister;