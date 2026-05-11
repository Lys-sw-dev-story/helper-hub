// src/pages/Assistant/AssistantRegister.tsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { registerAssistant, type AssistantData } from '../../api/assistantApi';

const AssistantRegister: React.FC = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<AssistantData>({
    assistant_name: '',
    assistant_phone: '',
    work_days: '',
    work_start_date: '',
    assistant_license: '',
    assistant_memo: '',
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
      alert('조력자 등록 성공!');
      navigate('/assistants');
    } catch (err) {
      alert('등록 실패! 필드명을 확인해 주세요.');
    }
  };

  return (
    <div style={{ padding: '2rem', maxWidth: '600px', margin: '0 auto' }}>
      <h2>🤝 조력자 신규 등록 (Backend Match)</h2>
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        <input name="assistant_name" placeholder="조력자 성함" onChange={handleChange} required />
        <input name="assistant_phone" placeholder="연락처" onChange={handleChange} />
        <input name="work_days" placeholder="근무 가능 요일 (예: 월,화,수)" onChange={handleChange} />
        <input name="work_start_date" type="date" onChange={handleChange} />
        <input name="assistant_license" placeholder="자격증 정보" onChange={handleChange} />
        <textarea name="assistant_memo" placeholder="메모" onChange={handleChange} rows={4} />
        <button type="submit" style={{ padding: '1rem', backgroundColor: '#34C759', color: 'white', border: 'none', borderRadius: '4px' }}>
          등록 완료
        </button>
      </form>
    </div>
  );
};

export default AssistantRegister;