from enum import StrEnum


RETENTION_YEARS = 5
AUDIT_WINDOW_YEARS = 2
EXPIRATION_WARNING_DAYS = 30
# 보관기간(5년) 만료 임박 경고 임계값. 만료예정(30일)과 분리된 전용 상수.
RETENTION_WARNING_DAYS = 180


class DocumentStatus(StrEnum):
    NOT_SUBMITTED = "미제출"
    SUBMITTED = "제출완료"  # CLAUDE.md §0.3 상태값 정합 (이전 "제출")
    EXPIRING_SOON = "만료예정"


class DocumentTargetType(StrEnum):
    ORGANIZATION = "organization"
    CLIENT = "client"
    ASSISTANT = "assistant"


class AssignmentStatus(StrEnum):
    ACTIVE = "active"
    ENDED = "ended"


class Weekday(StrEnum):
    """매칭 태그 1종: 요일 (이용자 희망 요일 ↔ 활동지원사 근무 가능 요일)."""

    MON = "월"
    TUE = "화"
    WED = "수"
    THU = "목"
    FRI = "금"
    SAT = "토"
    SUN = "일"


class SupportType(StrEnum):
    """매칭 태그 2종: 지원 분야 (이용자 희망 분야 ↔ 활동지원사 가능 분야)."""

    PHYSICAL = "신체활동 지원"
    HOUSEHOLD = "가사활동 지원"
    SOCIAL = "사회활동 지원"


# 태그 표준 정렬 순서 (표시/저장 정렬의 단일 출처)
WEEKDAY_ORDER: tuple[str, ...] = tuple(d.value for d in Weekday)
SUPPORT_TYPE_ORDER: tuple[str, ...] = tuple(s.value for s in SupportType)


def parse_tags(raw: str | None) -> list[str]:
    """CSV 문자열(예: "월,수,금")을 태그 리스트로 파싱. 공백·중복 제거(첫 등장 순서 유지)."""
    if not raw:
        return []
    result: list[str] = []
    for token in raw.split(","):
        tag = token.strip()
        if tag and tag not in result:
            result.append(tag)
    return result


def sort_tags(tags: list[str], order: tuple[str, ...]) -> list[str]:
    """표준 순서(order)에 맞춰 정렬. order 에 없는 값은 뒤에 원래 순서대로 붙인다."""
    index = {value: i for i, value in enumerate(order)}
    known = sorted((t for t in tags if t in index), key=lambda t: index[t])
    unknown = [t for t in tags if t not in index]
    return [*known, *unknown]
