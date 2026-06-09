import React from 'react';
import { parseTags, joinTags } from '../../lib/constants';
import './Tags.css';

type TagVariant = 'day' | 'support';

interface TagSelectorProps {
  options: readonly string[];
  value?: string | null; // CSV
  onChange: (csv: string) => void;
  variant?: TagVariant;
}

/** 등록/수정 폼에서 태그를 토글 선택하는 칩 그룹. 값은 CSV 문자열로 주고받는다. */
export const TagSelector: React.FC<TagSelectorProps> = ({
  options,
  value,
  onChange,
  variant = 'day',
}) => {
  const selected = parseTags(value);

  const toggle = (option: string) => {
    const next = selected.includes(option)
      ? selected.filter((t) => t !== option)
      : [...selected, option];
    // 표준 순서(options)로 재정렬해 저장
    const ordered = options.filter((o) => next.includes(o));
    onChange(joinTags(ordered));
  };

  return (
    <div className="tag-selector">
      {options.map((option) => {
        const isOn = selected.includes(option);
        return (
          <button
            type="button"
            key={option}
            className={`tag-chip tag-${variant} ${isOn ? 'selected' : ''}`}
            aria-pressed={isOn}
            onClick={() => toggle(option)}
          >
            {isOn ? '✓ ' : ''}
            {option}
          </button>
        );
      })}
    </div>
  );
};

interface TagChipsProps {
  tags?: string[] | string | null;
  variant?: TagVariant;
  highlight?: string[]; // 강조(매칭)할 태그 부분집합
  emptyText?: string;
}

/** 상세/목록에서 태그를 읽기 전용 칩으로 표시. highlight 에 든 태그는 강조한다. */
export const TagChips: React.FC<TagChipsProps> = ({
  tags,
  variant = 'day',
  highlight = [],
  emptyText = '-',
}) => {
  const list = Array.isArray(tags) ? tags : parseTags(tags);
  if (list.length === 0) {
    return <span className="tag-empty">{emptyText}</span>;
  }
  return (
    <span className="tag-chip-list">
      {list.map((tag) => (
        <span
          key={tag}
          className={`tag-chip tag-${variant} static ${
            highlight.includes(tag) ? 'matched' : ''
          }`}
        >
          {highlight.includes(tag) ? '✓ ' : ''}
          {tag}
        </span>
      ))}
    </span>
  );
};
