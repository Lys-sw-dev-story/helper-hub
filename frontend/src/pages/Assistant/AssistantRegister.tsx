import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { registerAssistant, type AssistantData } from '../../api/assistantApi';
import './AssistantRegister.css';

const AssistantRegister: React.FC = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<AssistantData>({
    assistant_name: '', assistant_phone: '', work_days: '',
    work_start_date: '', assistant_license: '', assistant_memo: '',
    organization_id: 1,
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await registerAssistant(formData);
      alert('활동지원사 등록 성공!');
      navigate('/assistants');
    } catch (err) {
      alert('등록 실패!');
    }
  };

  return (
    <div className="register-container">
      <h2>🤝 활동지원사 신규 등록 (Backend Match)</h2>
      <form onSubmit={handleSubmit} className="register-form">
        <input name="assistant_name" className="form-input" placeholder="활동지원사 성함" onChange={handleChange} required />
        <input name="assistant_phone" className="form-input" placeholder="연락처" onChange={handleChange} />
        <input name="work_days" className="form-input" placeholder="근무 가능 요일 (예: 월,화,수)" onChange={handleChange} />
        <input name="work_start_date" className="form-input" type="date" onChange={handleChange} />
        <input name="assistant_license" className="form-input" placeholder="자격증 정보" onChange={handleChange} />
        <textarea name="assistant_memo" className="form-textarea" placeholder="메모" onChange={handleChange} rows={4} />
        <button type="submit" className="submit-btn">등록 완료</button>
      </form>
    </div>
  );
};

export default AssistantRegister;