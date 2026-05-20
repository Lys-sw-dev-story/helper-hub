from enum import StrEnum


RETENTION_YEARS = 5
AUDIT_WINDOW_YEARS = 2
EXPIRATION_WARNING_DAYS = 30


class DocumentStatus(StrEnum):
    NOT_SUBMITTED = "미제출"
    SUBMITTED = "제출완료"
    NEEDS_REVISION = "보완필요"
    EXPIRING_SOON = "만료예정"
    EXPIRED = "만료"


class DocumentTargetType(StrEnum):
    ORGANIZATION = "organization"
    CLIENT = "client"
    ASSISTANT = "assistant"


class AssignmentStatus(StrEnum):
    ACTIVE = "active"
    ENDED = "ended"
