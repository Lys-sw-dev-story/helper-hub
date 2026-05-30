import React, { useEffect, useState } from 'react';
import { getAuditOverview, getAuditRecent } from '../../api/auditApi';
import type { AuditOverview, AuditRecentResponse, AuditDocumentItem } from '../../api/auditApi';
import './AuditPage.css';

type AuditTab = 'missing' | 'expiring_soon' | 'expired' | 'needs_revision' | 'retention_ending_soon';

const AuditPage: React.FC = () => {
  const [overview, setOverview] = useState<AuditOverview | null>(null);
  const [recent, setRecent] = useState<AuditRecentResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<AuditTab>('missing');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [overviewData, recentData] = await Promise.all([
          getAuditOverview(),
          getAuditRecent(),
        ]);
        setOverview(overviewData);
        setRecent(recentData);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <div className="audit-loading">🛡️ 공단 점검 및 감사 대비 지표 분석 중...</div>;
  if (!overview) return <div className="audit-error">점검 데이터를 불러오지 못했습니다.</div>;

  // 탭 클릭 시 렌더링할 타겟 배열 바인딩 함수
  const getActiveList = (): AuditDocumentItem[] => {
    switch (activeTab) {
      case 'missing': return overview.missing;
      case 'expiring_soon': return overview.expiring_soon;
      case 'expired': return overview.expired;
      case 'needs_revision': return overview.needs_revision;
      case 'retention_ending_soon': return overview.retention_ending_soon;
      default: return [];
    }
  };

  const currentList = getActiveList();

  return (
    <div className="audit-page-container">
      <div className="page-header">
        <h2>🛡️ 국민건강보험공단 점검 및 모니터링비 최적화</h2>
        <p>필수 서류 누락 및 유효기간 만료 상태를 영속적으로 모니터링하여 행정 처분을 예방합니다.</p>
      </div>

      {/* 1구역: 최근 2년 Cut-off 핵심 스냅샷 통계 바 */}
      <div className="recent-summary-strip">
        <div className="strip-title">
          📋 최근 <strong>{recent?.window_years}년</strong> 이내 데이터 동기화 현황
        </div>
        <div className="strip-grid">
          <div className="strip-item">이용자 <span>{recent?.clients.length}명</span></div>
          <div className="strip-item">활동지원사 <span>{recent?.assistants.length}명</span></div>
          <div className="strip-item">체크리스트 서류 <span>{recent?.documents.length}건</span></div>
          <div className="strip-item">이용일지 로그 <span>{recent?.service_logs.length}건</span></div>
        </div>
      </div>

      {/* 2구역: 5대 핵심 점검 요인 탭 바 컨트롤러 */}
      <div className="audit-tab-bar">
        <button className={`audit-tab missing ${activeTab === 'missing' ? 'active' : ''}`} onClick={() => setActiveTab('missing')}>
          ⚠️ 미제출 ({overview.missing.length})
        </button>
        <button className={`audit-tab expiring_soon ${activeTab === 'expiring_soon' ? 'active' : ''}`} onClick={() => setActiveTab('expiring_soon')}>
          ⏳ 만료예정 ({overview.expiring_soon.length})
        </button>
        <button className={`audit-tab expired ${activeTab === 'expired' ? 'active' : ''}`} onClick={() => setActiveTab('expired')}>
          🚨 기간만료 ({overview.expired.length})
        </button>
        <button className={`audit-tab needs_revision ${activeTab === 'needs_revision' ? 'active' : ''}`} onClick={() => setActiveTab('needs_revision')}>
          🔧 보완필요 ({overview.needs_revision.length})
        </button>
        <button className={`audit-tab retention ${activeTab === 'retention_ending_soon' ? 'active' : ''}`} onClick={() => setActiveTab('retention_ending_soon')}>
          📦 보관임박 ({overview.retention_ending_soon.length})
        </button>
      </div>

      {/* 3구역: 탭 하단 리스트 디테일 테이블 */}
      <div className="audit-detail-card">
        <table className="audit-table">
          <thead>
            <tr>
              <th>구분</th>
              <th>대상자명</th>
              <th>점검 필수 서류명</th>
              <th>작성(제출)일</th>
              <th>만료(예정)일</th>
              <th>남은 기한 / 상태</th>
            </tr>
          </thead>
          <tbody>
            {currentList.length === 0 ? (
              <tr>
                <td colSpan={6} className="empty-row">
                  🎉 해당 항목에 걸리는 위반 사항 또는 점검 대상 서류가 없습니다.
                </td>
              </tr>
            ) : (
              currentList.map((item, idx) => (
                <tr key={item.document_id || `missing-${idx}`} className="audit-row">
                  <td>
                    <span className={`target-badge ${item.target_type}`}>
                      {item.target_type === 'client' ? '이용자' : '지원사'}
                    </span>
                  </td>
                  <td className="name-cell">{item.target_name}</td>
                  <td className="doc-name-cell">{item.document_name}</td>
                  <td>{item.created_date || <span className="null-text">-</span>}</td>
                  <td>{item.expiration_date || <span className="null-text">-</span>}</td>
                  <td>
                    {activeTab === 'missing' && <span className="status-tag-red">서류미비</span>}
                    {activeTab === 'needs_revision' && <span className="status-tag-blue">수정·보완요망</span>}
                    {activeTab === 'expired' && <span className="status-tag-purple">효력상실</span>}
                    {activeTab === 'expiring_soon' && (
                      <span className="status-tag-orange">
                        {item.days_until_expire !== null ? `${item.days_until_expire}일 남음` : '만료임박'}
                      </span>
                    )}
                    {activeTab === 'retention_ending_soon' && (
                      <span className="status-tag-gray">
                        {item.days_until_retention_end !== null ? `보관종료 ${item.days_until_retention_end}일 전` : '보관임박'}
                      </span>
                    )}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default AuditPage;