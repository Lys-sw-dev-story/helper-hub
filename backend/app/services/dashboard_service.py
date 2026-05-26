from collections import Counter
from datetime import date

from sqlalchemy.orm import Session

from app.core.constants import AssignmentStatus, DocumentStatus, DocumentTargetType
from app.models.assignment import Assignment
from app.models.assistant import Assistant
from app.models.client import Client
from app.models.document import Document
from app.models.document_requirement import DocumentRequirement
from app.schemas.dashboard_schema import (
    DashboardCounts,
    DashboardSummary,
    DocumentStatusBarItem,
)
from app.services.document_service import compute_status


def _checklist_status_counter(
    db: Session,
    organization_id: int,
    today: date,
) -> Counter[DocumentStatus]:
    """모든 client/assistant 의 필수서류 체크리스트를 상태별로 합산한다."""
    counter: Counter[DocumentStatus] = Counter()

    # target_type 별 requirement 목록 미리 캐시
    client_reqs = (
        db.query(DocumentRequirement)
        .filter(DocumentRequirement.target_type == DocumentTargetType.CLIENT.value)
        .all()
    )
    assistant_reqs = (
        db.query(DocumentRequirement)
        .filter(DocumentRequirement.target_type == DocumentTargetType.ASSISTANT.value)
        .all()
    )

    # 모든 제출 문서 일괄 조회 후 (target_id, requirement_id) 로 인덱싱
    docs = (
        db.query(Document)
        .filter(Document.organization_id == organization_id)
        .all()
    )

    client_docs: dict[tuple[int, int], Document] = {}
    assistant_docs: dict[tuple[int, int], Document] = {}
    for doc in docs:
        if doc.requirement is None:
            continue
        key = (doc.target_id, doc.requirement_id)
        if doc.requirement.target_type == DocumentTargetType.CLIENT.value:
            client_docs[key] = doc
        elif doc.requirement.target_type == DocumentTargetType.ASSISTANT.value:
            assistant_docs[key] = doc

    clients = (
        db.query(Client.client_id)
        .filter(Client.organization_id == organization_id)
        .all()
    )
    for (client_id,) in clients:
        for req in client_reqs:
            doc = client_docs.get((client_id, req.requirement_id))
            if doc is None:
                counter[DocumentStatus.NOT_SUBMITTED] += 1
            else:
                counter[compute_status(doc, today)] += 1

    assistants = (
        db.query(Assistant.assistant_id)
        .filter(Assistant.organization_id == organization_id)
        .all()
    )
    for (assistant_id,) in assistants:
        for req in assistant_reqs:
            doc = assistant_docs.get((assistant_id, req.requirement_id))
            if doc is None:
                counter[DocumentStatus.NOT_SUBMITTED] += 1
            else:
                counter[compute_status(doc, today)] += 1

    return counter


def build_summary(
    db: Session, organization_id: int, today: date
) -> DashboardSummary:
    client_count = (
        db.query(Client)
        .filter(Client.organization_id == organization_id)
        .count()
    )
    assistant_count = (
        db.query(Assistant)
        .filter(Assistant.organization_id == organization_id)
        .count()
    )
    active_assignment_count = (
        db.query(Assignment)
        .join(Client, Assignment.client_id == Client.client_id)
        .filter(
            Client.organization_id == organization_id,
            Assignment.assignment_status == AssignmentStatus.ACTIVE.value,
        )
        .count()
    )

    counter = _checklist_status_counter(db, organization_id, today)

    chart = [
        DocumentStatusBarItem(status=status, count=counter.get(status, 0))
        for status in DocumentStatus
    ]

    return DashboardSummary(
        counts=DashboardCounts(
            client_count=client_count,
            assistant_count=assistant_count,
            active_assignment_count=active_assignment_count,
            not_submitted_document_count=counter.get(DocumentStatus.NOT_SUBMITTED, 0),
        ),
        document_status_chart=chart,
    )
