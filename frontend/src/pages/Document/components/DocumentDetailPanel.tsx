import type { IntegratedDocument } from '../types';

interface DocumentDetailPanelProps {
  documentItem: IntegratedDocument | null;
}

function DocumentDetailPanel({ documentItem }: DocumentDetailPanelProps) {
  if (!documentItem) {
    return (
      <aside className="document-detail-panel">
        <div className="document-detail-empty">문서를 선택하면 상세 정보가 표시됩니다.</div>
      </aside>
    );
  }

  const detailRows = [
    ['문서명', documentItem.documentName],
    ['문서유형', documentItem.documentType],
    ['이용자명', documentItem.clientName],
    ['활동지원사명', documentItem.assistantName],
    ['기준월', documentItem.baseMonth],
    ['등록일', documentItem.registeredAt],
    ['등록자', documentItem.registeredBy],
    ['상태', documentItem.status],
    ['파일명', documentItem.fileName],
    ['파일 형식', documentItem.fileType],
    ['파일 크기', documentItem.fileSize],
  ];

  return (
    <aside className="document-detail-panel">
      <div className="document-detail-header">
        <span>상세 정보</span>
        <strong>{documentItem.documentType}</strong>
      </div>

      <div className="document-detail-title">{documentItem.documentName}</div>

      <dl className="document-detail-list">
        {detailRows.map(([label, value]) => (
          <div key={label} className="document-detail-row">
            <dt>{label}</dt>
            <dd>{value}</dd>
          </div>
        ))}
      </dl>

      <div className="document-detail-actions">
        <button type="button">미리보기</button>
        <button type="button">다운로드</button>
        <button type="button">수정</button>
        <button type="button" className="danger">
          삭제
        </button>
        <button type="button">재업로드</button>
      </div>
    </aside>
  );
}

export default DocumentDetailPanel;