import React, { useEffect, useState } from 'react';
import {
  getChecklist,
  createDocument,
  updateDocument,
  replaceDocumentFile,
  DocumentTargetType,
  DocumentStatus,
  type DocumentChecklistItem
} from '../../api/documentApi';

interface DocumentSectionProps {
  targetType: DocumentTargetType;
  targetId: number;
  readOnly?: boolean;
}

const DocumentSection: React.FC<DocumentSectionProps> = ({ targetType, targetId, readOnly = false }) => {
  const [checklist, setChecklist] = useState<DocumentChecklistItem[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchChecklist = async () => {
    setLoading(true);
    try {
      const data = await getChecklist(targetType, targetId);
      setChecklist(data);
    } catch (err) {
      console.error(err);
      alert('서류 목록을 불러오지 못했습니다.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchChecklist();
  }, [targetType, targetId]);

  const handleFileUpload = async (requirementId: number, documentId: number | null | undefined, file: File) => {
    try {
      if (documentId) {
        await replaceDocumentFile(documentId, file);
        alert('파일이 성공적으로 업데이트되었습니다.');
      } else {
        await createDocument(requirementId, targetId, undefined, undefined, file);
        alert('파일이 성공적으로 등록되었습니다.');
      }
      fetchChecklist();
    } catch (err) {
      console.error(err);
      alert('파일 업로드에 실패했습니다.');
    }
  };

  const handleDateChange = async (requirementId: number, documentId: number | null | undefined, dateStr: string) => {
    try {
      if (documentId) {
        await updateDocument(documentId, { expiration_date: dateStr });
      } else {
        await createDocument(requirementId, targetId, dateStr, undefined, undefined);
      }
      fetchChecklist();
    } catch (err) {
      console.error(err);
      alert('만료일 업데이트에 실패했습니다.');
    }
  };

  if (loading) return <div>서류 목록 로딩 중...</div>;

  return (
    <div className="document-section" style={{ marginTop: '2rem' }}>
      <h3>📁 필수 서류 관리</h3>
      <table className="table" style={{ width: '100%', marginTop: '1rem', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th style={{ borderBottom: '2px solid #ddd', padding: '0.5rem', textAlign: 'left' }}>서류명</th>
            <th style={{ borderBottom: '2px solid #ddd', padding: '0.5rem', textAlign: 'left' }}>상태</th>
            <th style={{ borderBottom: '2px solid #ddd', padding: '0.5rem', textAlign: 'left' }}>만료일</th>
            {!readOnly && <th style={{ borderBottom: '2px solid #ddd', padding: '0.5rem', textAlign: 'left' }}>파일 업로드</th>}
          </tr>
        </thead>
        <tbody>
          {checklist.map((item) => (
            <tr key={item.requirement_id}>
              <td style={{ borderBottom: '1px solid #ddd', padding: '0.5rem' }}>{item.document_name}</td>
              <td style={{ borderBottom: '1px solid #ddd', padding: '0.5rem' }}>
                <span className={`status-badge ${item.status === DocumentStatus.NOT_SUBMITTED ? 'danger' : item.status === DocumentStatus.EXPIRING_SOON ? 'warning' : 'success'}`}>
                  {item.status}
                </span>
              </td>
              <td style={{ borderBottom: '1px solid #ddd', padding: '0.5rem' }}>
                {readOnly ? (
                  item.expiration_date || '-'
                ) : (
                  <input
                    type="date"
                    value={item.expiration_date || ''}
                    onChange={(e) => handleDateChange(item.requirement_id, item.document_id, e.target.value)}
                  />
                )}
              </td>
              {!readOnly && (
                <td style={{ borderBottom: '1px solid #ddd', padding: '0.5rem' }}>
                  <input
                    type="file"
                    onChange={(e) => {
                      if (e.target.files && e.target.files[0]) {
                        handleFileUpload(item.requirement_id, item.document_id, e.target.files[0]);
                      }
                    }}
                  />
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default DocumentSection;