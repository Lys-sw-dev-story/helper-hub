import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import {
  deleteAssistant,
  getAssistants,
  type AssistantDetail,
} from '../../api/assistantApi';
import './Assistant.css';

const AssistantList: React.FC = () => {
  const navigate = useNavigate();

  const [assistants, setAssistants] = useState<AssistantDetail[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchAssistants = async () => {
    try {
      setLoading(true);

      const data = await getAssistants();
      console.log('활동지원사 목록 조회 결과:', data);

      setAssistants(data);
    } catch (error) {
      console.error('활동지원사 목록 조회 실패:', error);
      setAssistants([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAssistants();
  }, []);

  const handleDelete = async (assistantId: number) => {
    const confirmed = window.confirm('정말 삭제하시겠습니까?');

    if (!confirmed) {
      return;
    }

    try {
      await deleteAssistant(assistantId);
      alert('활동지원사가 삭제되었습니다.');
      fetchAssistants();
    } catch (error) {
      console.error('활동지원사 삭제 실패:', error);
      const detail = axios.isAxiosError(error) ? error.response?.data?.detail : undefined;
      alert(typeof detail === 'string' ? detail : '삭제 실패! 다시 시도해 주세요.');
    }
  };

  return (
    <div className="assistant-card">
      <div className="page-header">
        <h2>🤝 활동지원사 관리 목록</h2>

        <button
          type="button"
          className="btn btn-primary"
          onClick={() => navigate('/assistants/register')}
        >
          + 신규 등록
        </button>
      </div>

      <table className="assistant-table">
        <thead>
          <tr>
            <th>성함</th>
            <th>소속 기관</th>
            <th>연락처</th>
            <th>근무 가능 요일</th>
            <th>관리</th>
          </tr>
        </thead>

        <tbody>
          {loading ? (
            <tr>
              <td colSpan={5}>불러오는 중입니다...</td>
            </tr>
          ) : assistants.length === 0 ? (
            <tr>
              <td colSpan={5}>등록된 활동지원사가 없습니다.</td>
            </tr>
          ) : (
            assistants.map((assistant) => (
              <tr key={assistant.assistant_id}>
                <td>{assistant.assistant_name}</td>
                <td>
                  {assistant.organization_id
                    ? `기관 #${assistant.organization_id}`
                    : '-'}
                </td>
                <td>{assistant.assistant_phone || '-'}</td>
                <td>{assistant.work_days || '-'}</td>
                <td>
                  <button
                    type="button"
                    className="btn btn-secondary"
                    onClick={() => navigate(`/assistants/${assistant.assistant_id}`)}
                  >
                    상세
                  </button>

                  <button
                    type="button"
                    className="btn btn-secondary"
                    onClick={() =>
                      navigate(`/assistants/${assistant.assistant_id}/edit`)
                    }
                  >
                    수정
                  </button>

                  <button
                    type="button"
                    className="btn btn-danger"
                    onClick={() => handleDelete(assistant.assistant_id)}
                  >
                    삭제
                  </button>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
};

export default AssistantList;