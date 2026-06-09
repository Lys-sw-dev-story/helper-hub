import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import {
  createAssignment,
  getMatchCandidates,
  type MatchCandidatesResponse,
} from '../../api/assignmentApi';
import { getClients, type ClientDetail } from '../../api/clientApi';
import { TagChips } from '../../components/common/Tags';
import './Assignment.css';

const AssignmentForm: React.FC = () => {
  const navigate = useNavigate();

  const [clients, setClients] = useState<ClientDetail[]>([]);
  const [selectedClientId, setSelectedClientId] = useState<string>('');
  const [match, setMatch] = useState<MatchCandidatesResponse | null>(null);
  const [loadingMatch, setLoadingMatch] = useState(false);
  const [selectedAssistantId, setSelectedAssistantId] = useState<number | null>(null);
  const [startDate, setStartDate] = useState('');
  const [submitting, setSubmitting] = useState(false);

  // 이용자 목록 로드 (1단계: 이용자 선택용)
  useEffect(() => {
    getClients()
      .then(setClients)
      .catch((err) => console.error(err));
  }, []);

  // 이용자 선택 시 → 태그 조건에 맞는 활동지원사 후보 조회 (2~3단계)
  useEffect(() => {
    if (!selectedClientId) {
      setMatch(null);
      setSelectedAssistantId(null);
      return;
    }
    let ignore = false;
    setLoadingMatch(true);
    setSelectedAssistantId(null);
    getMatchCandidates(Number(selectedClientId))
      .then((res) => {
        if (!ignore) setMatch(res);
      })
      .catch((err) => {
        if (ignore) return;
        console.error(err);
        setMatch(null);
        const detail = axios.isAxiosError(err) ? err.response?.data?.detail : undefined;
        alert(typeof detail === 'string' ? detail : '매칭 후보를 불러오지 못했습니다.');
      })
      .finally(() => {
        if (!ignore) setLoadingMatch(false);
      });
    return () => {
      ignore = true;
    };
  }, [selectedClientId]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!selectedClientId) {
      alert('먼저 이용자를 선택해 주세요.');
      return;
    }
    if (!selectedAssistantId) {
      alert('배정할 활동지원사를 선택해 주세요.');
      return;
    }
    if (!startDate) {
      alert('배정 시작일을 입력해 주세요.');
      return;
    }

    setSubmitting(true);
    try {
      await createAssignment({
        client_id: Number(selectedClientId),
        assistant_id: selectedAssistantId,
        start_date: startDate,
        end_date: null,
      });
      alert('🤝 매칭 배정이 성공적으로 등록되었습니다!');
      navigate('/assignments');
    } catch (err) {
      console.error(err);
      const detail = axios.isAxiosError(err) ? err.response?.data?.detail : undefined;
      alert(typeof detail === 'string' ? detail : '등록 실패: 서버 오류가 발생했습니다.');
    } finally {
      setSubmitting(false);
    }
  };

  const hasClientTags =
    !!match && (match.preferred_days.length > 0 || match.support_types.length > 0);

  return (
    <div className="assignment-form-container">
      <div className="form-card match-card">
        <h2>🤝 신규 매칭 배정 등록</h2>

        <form onSubmit={handleSubmit}>
          {/* 1단계: 이용자 선택 */}
          <div className="form-group">
            <label>① 이용자 선택 *</label>
            <select
              value={selectedClientId}
              onChange={(e) => setSelectedClientId(e.target.value)}
            >
              <option value="">-- 배정할 이용자를 선택하세요 --</option>
              {clients.map((c) => (
                <option key={c.client_id} value={c.client_id}>
                  {c.client_name}
                  {c.client_status ? ` (${c.client_status})` : ''}
                </option>
              ))}
            </select>
          </div>

          {/* 2단계: 선택한 이용자 이름 + 태그 표시 */}
          {match && (
            <div className="match-client-panel">
              <div className="match-client-head">
                <span className="match-client-name">{match.client_name}</span>
                <span className="match-client-sub">님의 매칭 조건</span>
              </div>
              <div className="match-tag-row">
                <span className="match-tag-label">희망 요일</span>
                <TagChips
                  tags={match.preferred_days}
                  variant="day"
                  emptyText="요일 조건 없음 (전체 표시)"
                />
              </div>
              <div className="match-tag-row">
                <span className="match-tag-label">희망 분야</span>
                <TagChips
                  tags={match.support_types}
                  variant="support"
                  emptyText="분야 조건 없음 (전체 표시)"
                />
              </div>
              {!hasClientTags && (
                <p className="match-hint">
                  ⓘ 이 이용자는 매칭 태그가 없어 모든 활동지원사가 후보로 표시됩니다.
                </p>
              )}
            </div>
          )}

          {/* 3단계: 조건에 맞는 활동지원사 후보 목록 (필터링됨) */}
          {selectedClientId && (
            <div className="form-group">
              <label>
                ② 조건에 맞는 활동지원사 선택 *
                {match && (
                  <span className="match-count"> · {match.candidate_count}명</span>
                )}
              </label>

              {loadingMatch ? (
                <div className="match-loading">조건에 맞는 활동지원사를 찾는 중...</div>
              ) : !match || match.candidate_count === 0 ? (
                <div className="match-empty">
                  조건에 맞는 활동지원사가 없습니다. 이용자의 희망 태그를 조정하거나
                  활동지원사 태그를 등록해 주세요.
                </div>
              ) : (
                <div className="candidate-list">
                  {match.candidates.map((cand) => {
                    const selected = selectedAssistantId === cand.assistant_id;
                    return (
                      <button
                        type="button"
                        key={cand.assistant_id}
                        className={`candidate-card ${selected ? 'selected' : ''}`}
                        onClick={() => setSelectedAssistantId(cand.assistant_id)}
                      >
                        <div className="candidate-head">
                          <span className="candidate-radio" aria-hidden>
                            {selected ? '◉' : '○'}
                          </span>
                          <span className="candidate-name">{cand.assistant_name}</span>
                          {cand.is_full_match ? (
                            <span className="badge badge-full">완전 매칭</span>
                          ) : (
                            <span className="badge badge-partial">부분 매칭</span>
                          )}
                          {cand.already_assigned && (
                            <span className="badge badge-assigned">이미 배정중</span>
                          )}
                        </div>
                        <div className="candidate-tags">
                          <span className="candidate-tag-label">요일</span>
                          <TagChips
                            tags={cand.work_days}
                            variant="day"
                            highlight={cand.matched_days}
                            emptyText="-"
                          />
                        </div>
                        <div className="candidate-tags">
                          <span className="candidate-tag-label">분야</span>
                          <TagChips
                            tags={cand.support_types}
                            variant="support"
                            highlight={cand.matched_support}
                            emptyText="-"
                          />
                        </div>
                      </button>
                    );
                  })}
                </div>
              )}
            </div>
          )}

          {/* 4단계: 배정 시작일 */}
          <div className="form-group">
            <label>③ 배정 시작일 *</label>
            <input
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
            />
          </div>

          <div className="form-actions">
            <button
              type="submit"
              className="btn btn-primary btn-block"
              disabled={submitting || !selectedAssistantId}
            >
              {submitting ? '등록 중...' : '매칭 등록하기 🔗'}
            </button>
            <button
              type="button"
              className="btn btn-secondary btn-block"
              onClick={() => navigate('/assignments')}
            >
              취소
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AssignmentForm;
