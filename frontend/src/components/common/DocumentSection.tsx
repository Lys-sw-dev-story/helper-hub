import React, { useEffect, useState } from 'react';
import {
  getChecklist,
  saveDocument,
  downloadDocument,
  DocumentTargetType,
  DocumentStatus,
  type DocumentChecklistItem
} from '../../api/documentApi';

interface DocumentSectionProps {
  targetType: DocumentTargetType;
  targetId: number;
  readOnly?: boolean;
}

interface RowEdit {
  file: File | null;
  expiration: string;
  created: string;
}

// 상태별 배지 색 (인라인 — 전역 CSS 의존 없이 일관 표시)
const statusBadgeStyle = (status: DocumentStatus): React.CSSProperties => {
  const base: React.CSSProperties = {
    padding: '3px 10px',
    borderRadius: '12px',
    fontSize: '0.8rem',
    fontWeight: 700,
    whiteSpace: 'nowrap',
  };
  if (status === DocumentStatus.NOT_SUBMITTED) return { ...base, background: '#fef2f2', color: '#ef4444' };
  if (status === DocumentStatus.EXPIRING_SOON) return { ...base, background: '#fffbeb', color: '#d97706' };
  return { ...base, background: '#ecfdf5', color: '#059669' }; // 제출완료
};

const linkBtnStyle: React.CSSProperties = {
  background: 'none',
  border: 'none',
  color: '#2563eb',
  cursor: 'pointer',
  padding: 0,
  fontSize: '0.88rem',
  textDecoration: 'underline',
};

const DocumentSection: React.FC<DocumentSectionProps> = ({ targetType, targetId, readOnly = false }) => {
  const [checklist, setChecklist] = useState<DocumentChecklistItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [edits, setEdits] = useState<Record<number, RowEdit>>({});
  const [savingId, setSavingId] = useState<number | null>(null);

  const fetchChecklist = async () => {
    setLoading(true);
    try {
      const data = await getChecklist(targetType, targetId);
      setChecklist(data);
      setEdits({});
    } catch (err) {
      console.error(err);
      alert('서류 목록을 불러오지 못했습니다.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchChecklist();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [targetType, targetId]);

  const getEdit = (item: DocumentChecklistItem): RowEdit =>
    edits[item.requirement_id] ?? { file: null, expiration: item.expiration_date || '', created: '' };

  const patchEdit = (item: DocumentChecklistItem, patch: Partial<RowEdit>) => {
    setEdits((prev) => {
      const current = prev[item.requirement_id] ?? { file: null, expiration: item.expiration_date || '', created: '' };
      return { ...prev, [item.requirement_id]: { ...current, ...patch } };
    });
  };

  const isDirty = (item: DocumentChecklistItem): boolean => {
    const e = edits[item.requirement_id];
    if (!e) return false;
    if (e.file) return true;
    if (e.created) return true;
    return (e.expiration || '') !== (item.expiration_date || '');
  };

  const handleSave = async (item: DocumentChecklistItem) => {
    const e = getEdit(item);
    // 신규 제출(기존 문서 없음)인데 파일 미선택 → 막는다 (만료일만으론 제출 처리 안 함)
    if (!item.document_id && !e.file) {
      alert('먼저 업로드할 파일을 선택해주세요.');
      return;
    }
    // 유효기간이 있는 서류는 만료일 필수
    if (item.valid_period_years && !e.expiration) {
      alert(`'${item.document_name}'은(는) 유효기간이 있는 서류입니다. 만료일을 입력한 뒤 저장해주세요.`);
      return;
    }
    setSavingId(item.requirement_id);
    try {
      await saveDocument({
        requirement_id: item.requirement_id,
        target_id: targetId,
        document_id: item.document_id ?? undefined,
        expiration_date: e.expiration || undefined,
        created_date: e.created || undefined,
        file: e.file ?? undefined,
      });
      await fetchChecklist();
      alert('변경사항이 저장되었습니다.');
    } catch (err) {
      console.error(err);
      alert('저장에 실패했습니다. 다시 시도해주세요.');
    } finally {
      setSavingId(null);
    }
  };

  const handleDownload = async (item: DocumentChecklistItem) => {
    if (!item.document_id) return;
    try {
      await downloadDocument(item.document_id, item.file_name);
    } catch (err) {
      console.error(err);
      alert('첨부된 파일이 없거나 다운로드에 실패했습니다.');
    }
  };

  if (loading) return <div>서류 목록 로딩 중...</div>;

  const cell: React.CSSProperties = { borderBottom: '1px solid #eee', padding: '0.6rem 0.5rem', verticalAlign: 'middle' };
  const headCell: React.CSSProperties = { borderBottom: '2px solid #ddd', padding: '0.6rem 0.5rem', textAlign: 'left' };

  return (
    <div className="document-section" style={{ marginTop: '2rem' }}>
      <h3>📁 필수 서류 관리</h3>
      <table className="table" style={{ width: '100%', marginTop: '1rem', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th style={headCell}>서류명</th>
            <th style={headCell}>상태</th>
            <th style={headCell}>첨부 파일</th>
            <th style={headCell}>만료일</th>
            {!readOnly && <th style={headCell}>파일 선택 / 저장</th>}
          </tr>
        </thead>
        <tbody>
          {checklist.map((item) => {
            const e = getEdit(item);
            const busy = savingId === item.requirement_id;
            const disabled = !isDirty(item) || busy;
            return (
              <tr key={item.requirement_id}>
                <td style={cell}>
                  {item.document_name}
                  {item.valid_period_years ? (
                    <span style={{ color: '#d97706', fontSize: '0.78rem', marginLeft: 6 }}>
                      (유효 {item.valid_period_years}년)
                    </span>
                  ) : null}
                </td>
                <td style={cell}>
                  <span style={statusBadgeStyle(item.status)}>{item.status}</span>
                </td>
                <td style={cell}>
                  {item.document_id && item.file_name ? (
                    <button type="button" style={linkBtnStyle} onClick={() => handleDownload(item)}>
                      ⬇ {item.file_name}
                    </button>
                  ) : (
                    <span style={{ color: '#bbb' }}>-</span>
                  )}
                  {!readOnly && e.file && (
                    <div style={{ fontSize: '0.78rem', color: '#2563eb', marginTop: 4 }}>
                      선택됨: {e.file.name}
                    </div>
                  )}
                </td>
                <td style={cell}>
                  {readOnly ? (
                    item.expiration_date || '-'
                  ) : (
                    <input
                      type="date"
                      value={e.expiration}
                      onChange={(ev) => patchEdit(item, { expiration: ev.target.value })}
                    />
                  )}
                </td>
                {!readOnly && (
                  <td style={cell}>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: 6, alignItems: 'flex-start' }}>
                      <label style={{ fontSize: '0.78rem', color: '#64748b' }}>
                        작성일{' '}
                        <input
                          type="date"
                          value={e.created}
                          onChange={(ev) => patchEdit(item, { created: ev.target.value })}
                        />
                      </label>
                      <div>
                        <input
                          type="file"
                          onChange={(ev) => patchEdit(item, { file: ev.target.files?.[0] ?? null })}
                        />
                        <button
                          type="button"
                          onClick={() => handleSave(item)}
                          disabled={disabled}
                          style={{
                            marginLeft: 8,
                            padding: '6px 12px',
                            borderRadius: 6,
                            border: 'none',
                            fontWeight: 600,
                            cursor: disabled ? 'not-allowed' : 'pointer',
                            background: disabled ? '#e2e8f0' : '#2563eb',
                            color: disabled ? '#94a3b8' : '#fff',
                          }}
                        >
                          {busy ? '저장 중...' : '변경사항 저장'}
                        </button>
                      </div>
                    </div>
                  </td>
                )}
              </tr>
            );
          })}
        </tbody>
      </table>
      {!readOnly && (
        <p style={{ marginTop: '0.8rem', fontSize: '0.82rem', color: '#64748b' }}>
          ※ 파일을 선택하고(유효기간 서류는 만료일도 입력한 뒤) <b>변경사항 저장</b>을 눌러야 반영됩니다.
          {' '}작성일은 비워두면 오늘로 저장됩니다 — 과거 날짜(예: 약 5년 전)로 지정하면 점검대비 <b>보관임박</b>에 노출됩니다.
        </p>
      )}
    </div>
  );
};

export default DocumentSection;
