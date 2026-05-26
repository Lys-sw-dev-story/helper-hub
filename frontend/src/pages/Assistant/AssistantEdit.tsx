import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getAssistant, updateAssistant, type AssistantData } from '../../api/assistantApi';
import './Assistant.css';

const AssistantEdit: React.FC = () => {
  const { assistantId: assistantIdParam } = useParams<{ assistantId: string }>();
  const navigate = useNavigate();
  const assistantId = Number(assistantIdParam);

  const [loading, setLoading] = useState(true);
  
  // 🚀 [해결 포인트] state 타입을 Partial<AssistantData>로 명시하여 organization_id 누락 에러 방지!
  const [formData, setFormData] = useState<Partial<AssistantData>>({
    assistant_name: '', 
    assistant_phone: '', 
    work_days: '',
    work_start_date: '', 
    assistant_license: '', 
    assistant_memo: '',
  });

  useEffect(() => {
    if (assistantId) {
      getAssistant(assistantId)
        .then((data) => {
          setFormData({
            assistant_name: data.assistant_name,
            assistant_phone: data.assistant_phone || '',
            work_days: data.work_days || '',
            work_start_date: data.work_start_date || '',
            assistant_license: data.assistant_license || '',
            assistant_memo: data.assistant_memo || '',
          });
          setLoading(false);
        })
        .catch((err) => {
          console.error(err);
          alert('데이터를 가져오는 데 실패했습니다.');
          navigate('/assistants');
        });
    }
  }, [assistantId, navigate]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      // 🚀 Partial 규격과 안전하게 싱크 완료!
      await updateAssistant(assistantId, formData);
      alert('활동지원사 정보가 성공적으로 변경되었습니다! 💾');
      navigate(`/assistants/${assistantId}`);
    } catch (err) {
      console.error(err);
      alert('정보 수정에 실패했습니다.');
    }
  };

  if (loading) return <div style={{ textAlign: 'center', padding: '3rem' }}>기존 데이터를 세팅 중...</div>;

  return (
    <div className="assistant-card">
      <div className="page-header">
        <h2>📝 활동지원사 프로필 수정</h2>
      </div>

      <form onSubmit={handleSubmit} className="assistant-form">
        <div className="form-group">
          <label>활동지원사 성함 (필수)</label>
          <input name="assistant_name" value={formData.assistant_name || ''} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>연락처</label>
          <input name="assistant_phone" value={formData.assistant_phone || ''} onChange={handleChange} />
        </div>
        <div className="form-group">
          <label>근무 가능 요일</label>
          <input name="work_days" value={formData.work_days || ''} onChange={handleChange} />
        </div>
        <div className="form-group">
          <label>업무 시작일</label>
          <input name="work_start_date" type="date" value={formData.work_start_date || ''} onChange={handleChange} />
        </div>
        <div className="form-group">
          <label>자격증 정보</label>
          <input name="assistant_license" value={formData.assistant_license || ''} onChange={handleChange} />
        </div>
        <div className="form-group">
          <label>메모 및 특이사항</label>
          <textarea name="assistant_memo" value={formData.assistant_memo || ''} onChange={handleChange} rows={4} />
        </div>

        <div className="btn-group">
          <button type="submit" className="btn btn-primary" style={{ flex: 1 }}>변경사항 저장 💾</button>
          <button type="button" className="btn btn-secondary" style={{ flex: 1 }} onClick={() => navigate(`/assistants/${assistantId}`)}>수정 취소</button>
        </div>
      </form>
    </div>
  );
};

export default AssistantEdit;