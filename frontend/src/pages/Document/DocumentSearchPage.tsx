import { useEffect, useMemo, useState } from 'react';
import { getIntegratedDocuments } from '../../api/documentApi';
import DocumentDetailPanel from './components/DocumentDetailPanel';
import DocumentFilter from './components/DocumentFilter';
import DocumentTable from './components/DocumentTable';
import type { DocumentFilterState, IntegratedDocument } from './types';
import './DocumentSearchPage.css';

const initialFilters: DocumentFilterState = {
  searchText: '',
  documentType: '전체',
  status: '전체',
  baseMonth: '',
  targetType: '전체',
};

function DocumentSearchPage() {
  const [documents, setDocuments] = useState<IntegratedDocument[]>([]);
  const [filters, setFilters] = useState<DocumentFilterState>(initialFilters);
  const [selectedDocumentId, setSelectedDocumentId] = useState<string | undefined>();
  const [checkedIds, setCheckedIds] = useState<Set<string>>(new Set());

  useEffect(() => {
    getIntegratedDocuments().then((result) => {
      setDocuments(result);
      setSelectedDocumentId(result[0]?.id);
    });
  }, []);

  const filteredDocuments = useMemo(() => {
    const searchKeyword = filters.searchText.trim().toLowerCase();

    return documents.filter((documentItem) => {
      const matchedSearch =
        searchKeyword.length === 0 ||
        documentItem.documentName.toLowerCase().includes(searchKeyword) ||
        documentItem.clientName.toLowerCase().includes(searchKeyword) ||
        documentItem.assistantName.toLowerCase().includes(searchKeyword);

      const matchedType =
        filters.documentType === '전체' || documentItem.documentType === filters.documentType;

      const matchedStatus =
        filters.status === '전체' || documentItem.status === filters.status;

      const matchedBaseMonth =
        filters.baseMonth.length === 0 || documentItem.baseMonth === filters.baseMonth;

      const matchedTargetType =
        filters.targetType === '전체' || documentItem.targetType === filters.targetType;

      return matchedSearch && matchedType && matchedStatus && matchedBaseMonth && matchedTargetType;
    });
  }, [documents, filters]);

  const selectedDocument =
    documents.find((documentItem) => documentItem.id === selectedDocumentId) ??
    filteredDocuments[0] ??
    null;

  const filteredDocumentIds = filteredDocuments.map((documentItem) => documentItem.id);
  const allChecked =
    filteredDocumentIds.length > 0 &&
    filteredDocumentIds.every((documentId) => checkedIds.has(documentId));

  const handleToggleCheck = (documentId: string) => {
    setCheckedIds((prev) => {
      const next = new Set(prev);
      if (next.has(documentId)) {
        next.delete(documentId);
      } else {
        next.add(documentId);
      }
      return next;
    });
  };

  const handleToggleAll = () => {
    setCheckedIds((prev) => {
      const next = new Set(prev);

      if (allChecked) {
        filteredDocumentIds.forEach((documentId) => next.delete(documentId));
      } else {
        filteredDocumentIds.forEach((documentId) => next.add(documentId));
      }

      return next;
    });
  };

  const handleReset = () => {
    setFilters(initialFilters);
    setCheckedIds(new Set());
    setSelectedDocumentId(documents[0]?.id);
  };

  const handleCreateDocument = () => {
    alert('문서 등록 기능은 추후 백엔드 API 연동 후 구현 예정입니다.');
  };

  const handleDownloadSelected = () => {
    alert(`${checkedIds.size}개 문서 다운로드 기능은 추후 구현 예정입니다.`);
  };

  const handleExportExcel = () => {
    alert('조회 결과 엑셀 다운로드 기능은 추후 구현 예정입니다.');
  };

  return (
    <main className="document-page">
      <header className="document-page-header">
        <div>
          <h1>문서 통합 조회</h1>
          <p>이용자, 활동지원사, 문서명, 문서 유형을 기준으로 문서를 통합 조회할 수 있습니다.</p>
        </div>
      </header>

      <DocumentFilter
        filters={filters}
        onChange={setFilters}
        onSearch={() => undefined}
        onReset={handleReset}
        onCreate={handleCreateDocument}
        onDownloadSelected={handleDownloadSelected}
        onExportExcel={handleExportExcel}
        selectedCount={checkedIds.size}
      />

      <section className="document-content-grid">
        <div className="document-list-panel">
          <div className="document-list-summary">
            <strong>조회 결과 {filteredDocuments.length}건</strong>
            <span>행을 클릭하면 오른쪽에서 상세 정보를 확인할 수 있습니다.</span>
          </div>

          <DocumentTable
            documents={filteredDocuments}
            selectedDocumentId={selectedDocument?.id}
            checkedIds={checkedIds}
            allChecked={allChecked}
            onSelectDocument={setSelectedDocumentId}
            onToggleCheck={handleToggleCheck}
            onToggleAll={handleToggleAll}
          />
        </div>

        <DocumentDetailPanel documentItem={selectedDocument} />
      </section>
    </main>
  );
}

export default DocumentSearchPage;