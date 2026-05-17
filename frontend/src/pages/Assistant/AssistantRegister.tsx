// frontend/src/pages/Assistant/AssistantRegister.tsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { registerAssistant, type AssistantData } from '../../api/assistantApi';
import './Assistant.css';

const AssistantRegister: React.FC = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<AssistantData>({
    assistant_name: '', assistant_phone: '', work_days: '',
    work_start_date: '', assistant_license: '', assistant_memo: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const submitData = { ...formData };
      if (!submitData.work_start_date) delete submitData.work_start_date;

      await registerAssistant(submitData);
      alert('활동지원사가 정상적으로 등록되었습니다! 🎉');
      navigate('/assistants');
    } catch (err) {
      console.error(err);
      alert('등록 실패! 입력 양식을 다시 확인해 주세요.');
    }
  };

  return (
    <div className="assistant-card">
      <div className="page-header">
        <h2>🤝 신규 활동지원사 등록</h2>
      </div>

      <form onSubmit={handleSubmit} className="assistant-form">
        <div className="form-group">
          <label>활동지원사 성함 (필수)</label>
          <input name="assistant_name" placeholder="이름을 입력하세요" onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>연락처</label>
          <input name="assistant_phone" placeholder="010-0000-0000" onChange={handleChange} />
        </div>
        <div className="form-group">
          <label>근무 가능 요일</label>
          <input name="work_days" placeholder="예: 월, 화, 수" onChange={handleChange} />
        </div>
        <div className="form-group">
          <label>업무 시작일</label>
          <input name="work_start_date" type="date" onChange={handleChange} />
        </div>
        <div className="form-group">
          <label>자격증 정보</label>
          <input name="assistant_license" placeholder="보유 자격증 기재" onChange={handleChange} />
        </div>
        <div className="form-group">
          <label>메모 및 특이사항</label>
          <textarea name="assistant_memo" placeholder="비고 사항 입력" onChange={handleChange} rows={4} />
        </div>

        <div className="btn-group">
          <button type="submit" className="btn btn-success" style={{ flex: 1 }}>등록 완료 💾</button>
          <button type="button" className="btn btn-secondary" style={{ flex: 1 }} onClick={() => navigate('/assistants')}>취소</button>
        </div>
      </form>
    </div>
  );
};

export default AssistantRegister;