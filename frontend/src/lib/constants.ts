// 매칭 태그 상수 (백엔드 app/core/constants.py 와 동기 유지할 단일 출처)
// - 요일: 이용자 희망 요일 ↔ 활동지원사 근무 가능 요일
// - 지원 분야: 이용자 희망 분야 ↔ 활동지원사 가능 분야

export const WEEKDAYS = ['월', '화', '수', '목', '금', '토', '일'] as const;
export type Weekday = (typeof WEEKDAYS)[number];

export const SUPPORT_TYPES = [
  '신체활동 지원',
  '가사활동 지원',
  '사회활동 지원',
] as const;
export type SupportType = (typeof SUPPORT_TYPES)[number];

// 서류 보관/점검 관련 상수 (백엔드와 동기). 현재는 태그 매칭에서 미사용이나
// CLAUDE.md §4 "상수는 한 곳에 모은다" 에 따라 프론트 단일 출처로 둔다.
export const RETENTION_YEARS = 5;
export const AUDIT_WINDOW_YEARS = 2;
export const EXPIRATION_WARNING_DAYS = 30;

const orderComparator = (order: readonly string[]) => {
  const index = new Map(order.map((value, i) => [value, i]));
  return (a: string, b: string) =>
    (index.get(a) ?? Number.MAX_SAFE_INTEGER) -
    (index.get(b) ?? Number.MAX_SAFE_INTEGER);
};

/** CSV 문자열(예: "월,수,금")을 태그 배열로 파싱. 공백·중복 제거(첫 등장 순서 유지). */
export const parseTags = (raw?: string | null): string[] => {
  if (!raw) return [];
  const result: string[] = [];
  for (const token of raw.split(',')) {
    const tag = token.trim();
    if (tag && !result.includes(tag)) result.push(tag);
  }
  return result;
};

/** 태그 배열을 저장용 CSV 문자열로 직렬화. */
export const joinTags = (tags: string[]): string => tags.join(',');

/** 표준 순서로 정렬(요일). */
export const sortWeekdays = (tags: string[]): string[] =>
  [...tags].sort(orderComparator(WEEKDAYS));

/** 표준 순서로 정렬(지원 분야). */
export const sortSupport = (tags: string[]): string[] =>
  [...tags].sort(orderComparator(SUPPORT_TYPES));
