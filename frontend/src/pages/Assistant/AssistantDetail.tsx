import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getAssistant, deleteAssistant, type AssistantData } from '../../api/assistantApi';
import './Assistant.css';

const AssistantDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const assistantId = Number(id);

  const [loading, setLoading] = useState(true);
  const [data, setData] = useState<AssistantData | null>(null);

  useEffect(() => {
    if (assistantId) {
      getAssistant(assistantId)
        .then((res) => {
          setData(res);
          setLoading(false);
        })
        .catch((err) => {
          console.error(err);
          alert('데이터를 가져오지 못했습니다.');
          navigate('/assistants');
        });
    }
  }, [assistantId, navigate]);

  const handleDelete = async () => {
    if (window.confirm('정말로 이 활동지원사 정보를 완전히 삭제하시겠습니까?')) {
      try {
        await deleteAssistant(assistantId);
        alert('성공적으로 삭제되었습니다.');
        navigate('/assistants');
      } catch (err) {
        console.error(err);
        alert('삭제에 실패했습니다.');
      }
    }
  };

  if (loading) return <div style={{ textAlign: 'center', padding: '3rem' }}>정보를 불러오는 중...</div>;
  if (!data) return <div style={{ textAlign: 'center', padding: '3rem' }}>데이터가 존재하지 않습니다.</div>;

  return (
    <div className="assistant-card">
      {/* 스타일 대문자 카멜케이스로 완벽 수정 */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <h2>🔍 활동지원사 상세 프로필</h2>
        <button onClick={handleDelete} className="btn btn-danger">정보 삭제 🗑️</button>
      </div>

      <div className="assistant-form">
        <div className="form-group">
          <label>성함</label>
          <div className="detail-value" style={{ fontWeight: 'bold' }}>{data.assistant_name}</div>
        </div>
        <div className="form-group">
          <label>연락처</label>
          <div className="detail-value">{data.assistant_phone || '-'}</div>
        </div>
        <div className="form-group">
          <label>근무 가능 요일</label>
          <div className="detail-value">{data.work_days || '-'}</div>
        </div>
        <div className="form-group">
          <label>업무 시작일</label>
          <div className="detail-value">{data.work_start_date || '-'}</div>
        </div>
        <div className="form-group">
          <label>자격증 정보</label>
          <div className="detail-value">{data.assistant_license || '-'}</div>
        </div>
        <div className="form-group">
          <label>메모 및 특이사항</label>
          <div className="detail-value memo">{data.assistant_memo || '등록된 특이사항이 없습니다.'}</div>
        </div>

        <div className="btn-group">
          <button type="button" className="btn btn-primary" style={{ flex: 1 }} onClick={() => navigate(`/assistants/${assistantId}/edit`)}>
            정보 수정하러 가기 ✏️
          </button>
          <button type="button" className="btn btn-secondary" style={{ flex: 1 }} onClick={() => navigate('/assistants')}>
            목록으로 돌아가기
          </button>
        </div>
      </div>
    </div>
  );
};

export default AssistantDetail;