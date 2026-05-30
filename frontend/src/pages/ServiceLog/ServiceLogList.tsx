import React, { useEffect, useState } from 'react';
import { listServiceLogs } from '../../api/serviceLogApi';
import type { ServiceLogResponse } from '../../api/serviceLogApi';
import './ServiceLogList.css';

const ServiceLogList: React.FC = () => {
  const [logs, setLogs] = useState<ServiceLogResponse[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const data = await listServiceLogs();
        setLogs(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchLogs();
  }, []);

  if (loading) return <div className="loading-box">이용내역을 불러오는 중... 🚀</div>;

  return (
    <div className="servicelog-container">
      <div className="page-header">
        <h2>🗓️ 사회복지 서비스 제공 내역 관리</h2>
        <p>배정된 이용자와 활동지원사의 일별 일지 등록 내역을 검토합니다.</p>
      </div>

      <div className="servicelog-card">
        <table className="servicelog-table">
          <thead>
            <tr>
              <th>일지 ID</th>
              <th>서비스 제공일</th>
              <th>이용자 (고객명)</th>
              <th>활동지원사</th>
              <th>제공 시간</th>
              <th>제공 횟수</th>
              <th>주요 서비스 수행 내용</th>
            </tr>
          </thead>
          <tbody>
            {logs.length === 0 ? (
              <tr>
                <td colSpan={7} className="empty-row">
                  등록된 서비스 이용내역 일지가 존재하지 않습니다.
                </td>
              </tr>
            ) : (
              logs.map((log) => (
                <tr key={log.service_log_id} className="servicelog-row">
                  <td className="log-id-cell">#{log.service_log_id}</td>
                  <td className="date-cell">{log.service_date}</td>
                  <td className="client-name-cell">{log.client_name}</td>
                  <td className="assistant-name-cell">{log.assistant_name}</td>
                  <td className="hours-cell">
                    <span className="hours-badge">{log.service_hours}시간</span>
                  </td>
                  <td className="count-cell">{log.service_count ?? '-'}회</td>
                  <td className="content-cell" title={log.service_content || ''}>
                    {log.service_content ?? <span className="no-content">작성 내용 없음</span>}
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

export default ServiceLogList;