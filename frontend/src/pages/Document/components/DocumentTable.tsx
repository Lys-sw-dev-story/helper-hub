import type { IntegratedDocument } from '../types';

interface DocumentTableProps {
  documents: IntegratedDocument[];
  selectedDocumentId?: string;
  checkedIds: Set<string>;
  allChecked: boolean;
  onSelectDocument: (documentId: string) => void;
  onToggleCheck: (documentId: string) => void;
  onToggleAll: () => void;
}

const statusClassNameMap: Record<IntegratedDocument['status'], string> = {
  정상: 'status-normal',
  '검토 필요': 'status-review',
  누락: 'status-missing',
  '만료 예정': 'status-expiring',
};

function DocumentTable({
  documents,
  selectedDocumentId,
  checkedIds,
  allChecked,
  onSelectDocument,
  onToggleCheck,
  onToggleAll,
}: DocumentTableProps) {
  if (documents.length === 0) {
    return <div className="document-empty">조회된 문서가 없습니다.</div>;
  }

  return (
    <div className="document-table-wrapper">
      <table className="document-table">
        <thead>
          <tr>
            <th>
              <input
                type="checkbox"
                checked={allChecked}
                onChange={onToggleAll}
                aria-label="전체 문서 선택"
              />
            </th>
            <th>문서명</th>
            <th>문서유형</th>
            <th>이용자명</th>
            <th>활동지원사명</th>
            <th>기준월</th>
            <th>등록일</th>
            <th>상태</th>
            <th>관리</th>
          </tr>
        </thead>
        <tbody>
          {documents.map((documentItem) => (
            <tr
              key={documentItem.id}
              className={selectedDocumentId === documentItem.id ? 'selected-row' : ''}
              onClick={() => onSelectDocument(documentItem.id)}
            >
              <td onClick={(event) => event.stopPropagation()}>
                <input
                  type="checkbox"
                  checked={checkedIds.has(documentItem.id)}
                  onChange={() => onToggleCheck(documentItem.id)}
                  aria-label={`${documentItem.documentName} 선택`}
                />
              </td>
              <td className="document-name-cell">{documentItem.documentName}</td>
              <td>{documentItem.documentType}</td>
              <td>{documentItem.clientName}</td>
              <td>{documentItem.assistantName}</td>
              <td>{documentItem.baseMonth}</td>
              <td>{documentItem.registeredAt}</td>
              <td>
                <span className={`document-status-badge ${statusClassNameMap[documentItem.status]}`}>
                  {documentItem.status}
                </span>
              </td>
              <td onClick={(event) => event.stopPropagation()}>
                <button
                  type="button"
                  className="document-table-action"
                  onClick={() => onSelectDocument(documentItem.id)}
                >
                  보기
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default DocumentTable;