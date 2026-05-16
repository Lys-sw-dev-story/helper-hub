import type { ChangeEvent } from 'react';
import type {
  DocumentFilterState,
  DocumentStatusFilter,
  DocumentTypeFilter,
  TargetTypeFilter,
} from '../types';

interface DocumentFilterProps {
  filters: DocumentFilterState;
  onChange: (nextFilters: DocumentFilterState) => void;
  onSearch: () => void;
  onReset: () => void;
  onCreate: () => void;
  onDownloadSelected: () => void;
  onExportExcel: () => void;
  selectedCount: number;
}

const documentTypes: DocumentTypeFilter[] = [
  '전체',
  '계약서',
  '이용내역서',
  '제공기록지',
  '개인정보동의서',
  '급여제공계획서',
  '기타',
];

const statuses: DocumentStatusFilter[] = ['전체', '정상', '검토 필요', '누락', '만료 예정'];
const targetTypes: TargetTypeFilter[] = ['전체', '이용자', '활동지원사'];

function DocumentFilter({
  filters,
  onChange,
  onSearch,
  onReset,
  onCreate,
  onDownloadSelected,
  onExportExcel,
  selectedCount,
}: DocumentFilterProps) {
  const updateFilter = (name: keyof DocumentFilterState, value: string) => {
    onChange({
      ...filters,
      [name]: value,
    });
  };

  const handleInputChange = (event: ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    updateFilter(event.target.name as keyof DocumentFilterState, event.target.value);
  };

  return (
    <section className="document-filter-panel">
      <div className="document-search-row">
        <input
          className="document-search-input"
          name="searchText"
          value={filters.searchText}
          onChange={handleInputChange}
          placeholder="문서명, 이용자명, 활동지원사명으로 검색"
        />
        <button type="button" className="document-primary-button" onClick={onSearch}>
          검색
        </button>
        <button type="button" className="document-secondary-button" onClick={onReset}>
          초기화
        </button>
        <button type="button" className="document-primary-button" onClick={onCreate}>
          문서 등록
        </button>
      </div>

      <div className="document-filter-row">
        <label>
          문서 유형
          <select name="documentType" value={filters.documentType} onChange={handleInputChange}>
            {documentTypes.map((type) => (
              <option key={type} value={type}>
                {type}
              </option>
            ))}
          </select>
        </label>

        <label>
          문서 상태
          <select name="status" value={filters.status} onChange={handleInputChange}>
            {statuses.map((status) => (
              <option key={status} value={status}>
                {status}
              </option>
            ))}
          </select>
        </label>

        <label>
          기준월
          <input
            type="month"
            name="baseMonth"
            value={filters.baseMonth}
            onChange={handleInputChange}
          />
        </label>

        <label>
          대상자 유형
          <select name="targetType" value={filters.targetType} onChange={handleInputChange}>
            {targetTypes.map((targetType) => (
              <option key={targetType} value={targetType}>
                {targetType}
              </option>
            ))}
          </select>
        </label>
      </div>

      <div className="document-bulk-actions">
        <span>선택된 문서 {selectedCount}개</span>
        <button
          type="button"
          className="document-secondary-button"
          onClick={onDownloadSelected}
          disabled={selectedCount === 0}
        >
          선택 문서 다운로드
        </button>
        <button type="button" className="document-secondary-button" onClick={onExportExcel}>
          조회 결과 엑셀 다운로드
        </button>
      </div>
    </section>
  );
}

export default DocumentFilter;