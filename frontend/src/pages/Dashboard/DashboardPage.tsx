import React, { useEffect, useState } from 'react';
import { getDashboardSummary } from '../../api/dashboardApi';
import type { DashboardSummary } from '../../api/dashboardApi';
import './DashboardPage.css';

const DashboardPage: React.FC = () => {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const data = await getDashboardSummary();
        setSummary(data);
      } catch (err: any) {
        setError(err.message || '대시보드 데이터를 불러오는데 실패했습니다.');
      } finally {
        setLoading(false);
      }
    };
    fetchSummary();
  }, []);

  if (loading) return <div className="dashboard-loading">대시보드 로딩 중... 🚀</div>;
  if (error) return <div className="dashboard-error">오류: {error}</div>;
  if (!summary) return <div className="dashboard-empty">데이터가 없습니다.</div>;

  const { counts, document_status_chart } = summary;

  // 백엔드 상태값을 직관적인 한글 타이틀로 매핑
  const statusLabels: Record<string, string> = {
    '미제출': '미제출 서류',
    '제출완료': '제출완료 (정상)',
    '만료예정': '만료임박 (보완요망)',
    '만료': '기간만료 (재제출 필요)',
    '보완필요': '보완필요 상태',
  };

  // 백엔드 상태값을 CSS 클래스명으로 매핑
  const statusClasses: Record<string, string> = {
    '미제출': 'not_submitted',
    '제출완료': 'submitted',
    '만료예정': 'expiring_soon',
    '만료': 'expired',
    '보완필요': 'needs_revision',
  };

  return (
    <div className="dashboard-page-container">
      <div className="page-header">
        <h2>📊 Helper-Hub 운영 대시보드</h2>
        <p>실시간 이용자 현황 및 필수 서류 점검 지표를 한눈에 모니터링합니다.</p>
      </div>

      {/* 4분할 핵심 스펙 통계 카드 카드 */}
      <div className="summary-cards-grid">
        <div className="summary-card">
          <h3>등록 이용자</h3>
          <p className="card-number">{counts.client_count}<span>명</span></p>
        </div>
        <div className="summary-card">
          <h3>활동지원사</h3>
          <p className="card-number">{counts.assistant_count}<span>명</span></p>
        </div>
        <div className="summary-card">
          <h3>활성 매칭 배정</h3>
          <p className="card-number active-color">{counts.active_assignment_count}<span>건</span></p>
        </div>
        <div className="summary-card alert-card">
          <h3>미제출 필수서류</h3>
          <p className="card-number danger-color">{counts.not_submitted_document_count}<span>건</span></p>
        </div>
      </div>

      {/* 게이지 바 차트 섹션 */}
      <div className="chart-section">
        <h3>📑 기관 필수서류 점검 및 분포 현황</h3>
        <div className="status-bars-container">
          {document_status_chart.map((item) => {
            // 유연한 비율 렌더링을 위한 임시 스케일 계산 (데이터가 적어도 시각적 바 노출되도록 보정)
            const fillWidth = item.count > 0 ? Math.max((item.count / 20) * 100, 8) : 0;
            
            return (
              <div key={item.status} className="status-bar-row">
                <span className="status-label">{statusLabels[item.status] || item.status}</span>
                <div className="bar-track">
                  <div 
                    className={`bar-fill ${statusClasses[item.status] || ''}`} 
                    style={{ width: `${Math.min(fillWidth, 100)}%` }}
                  ></div>
                </div>
                <span className="status-count">{item.count}건</span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;