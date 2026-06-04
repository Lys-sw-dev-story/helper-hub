import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { registerAssistant, type AssistantData } from '../../api/assistantApi';
import './AssistantRegister.css';

const AssistantRegister: React.FC = () => {
  const navigate = useNavigate();

  const [formData, setFormData] = useState<Omit<AssistantData, 'organization_id'>>({
    assistant_name: '',
    assistant_phone: '',
    work_days: '',
    work_start_date: '',
    assistant_license: '',
    assistant_memo: '',
  });

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    try {
      // 🔥 [해결책] 로컬 스토리지 등에 저장된 로그인 유저 정보에서 organization_id를 동적으로 가져옴
      const storedUser = localStorage.getItem('user');
      const userObj = storedUser ? JSON.parse(storedUser) : null;
      const currentOrgId = userObj?.organization_id || 1;

      const submitData: AssistantData = {
        assistant_name: formData.assistant_name,
        assistant_phone: formData.assistant_phone || undefined,
        work_days: formData.work_days || undefined,
        work_start_date: formData.work_start_date || undefined,
        assistant_license: formData.assistant_license || undefined,
        assistant_memo: formData.assistant_memo || undefined,
        organization_id: currentOrgId, // 🔐 하드코딩 1 대신 현재 로그인한 기관 ID 동적 주입!
      };

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
          <label htmlFor="assistant_name">활동지원사 성함 (필수)</label>
          <input
            id="assistant_name"
            name="assistant_name"
            placeholder="이름 입력"
            value={formData.assistant_name}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="assistant_phone">연락처</label>
          <input id="assistant_phone" name="assistant_phone" placeholder="010-0000-0000" value={formData.assistant_phone} onChange={handleChange} />
        </div>

        <div className="form-group">
          <label htmlFor="work_days">근무 가능 요일</label>
          <input id="work_days" name="work_days" placeholder="예: 월, 수, 금" value={formData.work_days} onChange={handleChange} />
        </div>

        <div className="form-group">
          <label htmlFor="work_start_date">업무 시작일</label>
          <input id="work_start_date" name="work_start_date" type="date" value={formData.work_start_date} onChange={handleChange} />
        </div>

        <div className="form-group">
          <label htmlFor="assistant_license">자격증 정보</label>
          <input id="assistant_license" name="assistant_license" placeholder="자격증 정보 입력" value={formData.assistant_license} onChange={handleChange} />
        </div>

        <div className="form-group">
          <label htmlFor="assistant_memo">메모 및 특이사항</label>
          <textarea id="assistant_memo" name="assistant_memo" placeholder="상세 비고 내용 입력" value={formData.assistant_memo} onChange={handleChange} rows={4} />
        </div>

        <div className="btn-group" style={{ marginTop: '2rem' }}>
          <button type="submit" className="btn btn-success" style={{ flex: 1 }}>등록 완료 💾</button>
          <button type="button" className="btn btn-secondary" style={{ flex: 1 }} onClick={() => navigate('/assistants')}>취소</button>
        </div>
      </form>
    </div>
  );
};

export default AssistantRegister;